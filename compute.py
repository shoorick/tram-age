import sys
import re
import urllib.request
from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup

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
def get_content(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' +
                '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req)
    return f.read().decode('utf-8')

def main():
    check_version()
    trams = {}
    total = 0
    title = ''

    # TODO read from command line
    city = 54 # Chelyabinsk
    kind =  1 # tram, 2 trolleybus, 3 subway, 4 monorail, 5 funicular, 6 translohr
            # 7 mover, 8 maglev, 9 electic bus
    service = 0 # only for passengers

    url = urljoin(
        'https://transphoto.org/list.php',
        '?' + urlencode({'t': kind, 'cid': city, 'serv': service}))

    while url:
        soup = BeautifulSoup(get_content(url), 'lxml')

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

                built = cells[3].text   # YYYY or mm.YYYY
                year = built[-4:]       # drop month if exists
                trams[year] = trams.get(year, 0) + 1
                total += 1

    if trams:
        print(title, '-' * len(title), sep='\n')

        for year in sorted(trams):
            print(year, trams[year], '#' * trams[year], sep='\t')

        print('-' * 16)
        print('Total', total, sep='\t')

    else:
        print('No data')


if __name__ == '__main__':
    main()
