import argparse
import numpy as np
import pandas as pd
import re
import sys
import urllib.request
import yaml
from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup
from transliterate import translit

"""
Check for version of Python and exit with error when version is older than 3
"""
def check_version():
    major_version = int(re.search('^\d+', sys.version).group(0))
    if major_version < 3:
        sys.exit('Use version 3 at least\n')

"""
Get content from specified URL
"""
def get_content(url, language):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
                '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Cookie': 'lang={}'.format(language)
        }
    )

    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')

"""
Parse command line arguments or print usage information
"""
def parse_arguments():
    parser = argparse.ArgumentParser(description='Gather and process public transportation data from transphoto.org')
    parser.add_argument('-c', '--city',
                        help='number or name (default city is Moscow)',
                        default='')
    parser.add_argument('-t', '--type',
                        help='transportation type (1-9 or name, default value is tram)',
                        default='')
    parser.add_argument('-l', '--language',
                        dest='code',
                        help='ISO 639-1 language code (default is ru for Russian)',
                        default='')
    parser.add_argument('-o', '--output',
                        dest='file',
                        help='output frequency table to file')
    return parser.parse_args()

"""
Main function
"""
def main():
    check_version()
    years = []
    total = 0
    title = ''

    with open('config.yml') as file:
        config = yaml.full_load(file)

    """
    Parse arguments
    and search for appropriate codes of city and transportation type
    """
    args = parse_arguments()

    language = args.code
    lang = re.search(r'^([a-z]{2})', language)
    language = lang.group(0) if lang else config.get('language');

    city = args.city
    if not re.match(r'^\d+$', city):
        # try to guess id by name
        cities = config.get('cities')

        # append dictionary of cities, read data from web
        soup  = BeautifulSoup(get_content(config.get('url')['cities'], language), 'lxml')
        table = soup.find('div', attrs={'class': 'p20w'})
        links = table.find_all('a')

        for link in links:
            city_name = link.text.lower()
            id = re.search(r'\d+', link.get('href'))
            if id:
                city_id = id.group(0)
                cities[city_name] = city_id

                if re.match(r'[А-ЯЁ]', city_name, re.I):
                    transliterated = translit(city_name, reversed=True)
                    cities[transliterated] = city_id

                    if 'j' in transliterated:
                        cities[transliterated.replace('j', 'y')] = city_id

        city = cities.get(city.lower(), cities['default'])

    kind = args.type
    if not re.match(r'^\d+$', kind):
        kinds = config.get('types')
        kind = kinds.get(kind.lower(), kinds['default'])

    output = args.file
    if output and not re.search(r'\.(csv|html?|js(on)?|xlsx?)$', output, re.I):
        sys.exit('Output file {} has unknown type. '
            + 'Only CSV, HTML, and XSLX are available.\n'.format(output))

    service = 0 # only for passengers

    url = urljoin(
        config.get('url')['wagons'],
        '?' + urlencode({'t': kind, 'cid': city, 'serv': service}))

    while url:
        soup = BeautifulSoup(get_content(url, language), 'lxml')

        next_link = soup.find('a', attrs={'id': 'NextLink'})
        url = urljoin(url, next_link.get('href')) if next_link else None

        if not title:
            title = soup.find('h2').text

        # get tables wrapped by div.rtable
        tables = soup.find_all('div', attrs={'class': 'rtable'})

        for table in tables:
            rows = table.find_all('tr')

            for row in rows:
                row_classes = row.get('class')
                # suitable rows has class s1 or s11
                if not ('s1' in row_classes or 's11' in row_classes):
                    continue

                cells = row.find_all('td')
                if not cells:
                    continue
                    # header row doesn't contain any <td> cells

                built = cells[3].text   # YYYY, mm.YYYY or YYYY-mm
                if built:
                    matched = re.search(r'\d{4}', built)
                    if matched:
                        years.append(int(matched.group(0)))

    if years:
        series = pd.Series(years)
        counts = pd.DataFrame({'count': series.value_counts()}).sort_index()

        if output:
            if re.search(r'\.csv$', output, re.I):
                counts.to_csv(output)
            elif re.search(r'\.html?$', output, re.I):
                counts.to_html(output)
            elif re.search(r'\.js(on)?$', output, re.I):
                counts.to_json(output)
            elif re.search(r'\.xlsx?$', output, re.I):
                counts.to_excel(output)
        else:
            print(title, '-' * len(title), sep='\n')
            for year, count in counts['count'].items():
                print('{:<4}  {:>6} {}'.format(year, count, '#' * count))

            print('-' * 12) # year + gap + count

        print('Total {:>6}'.format(len(years)))
        print(
            'Mean: {:.5}, median: {:.5}, modes: {}'.format(
                series.mean(),
                series.quantile(), # median
                series.mode().to_list(),
            )
        )

    else:
        print('No data')


if __name__ == '__main__':
    main()
