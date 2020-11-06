import sys
import re
import urllib.request
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
    soup = BeautifulSoup(
        get_content('https://transphoto.org/list.php?t=1&cid=54&sort=built&serv=0'),
        'lxml')

    # get first table wrapped by div.rtable
    table = soup.find('div', attrs={'class': 'rtable'})
    if not table:
        sys.exit("Can't find table wrapper")

    trams = {}

    rows = table.find_all('tr')
    if not rows:
        sys.exit("Can't find any rows")

    for row in rows:
        cells = row.find_all('td')
        if not cells:
            continue
            # header row doesn't contain any <td> cells

        # passenger trams has 4-digit numbers
        if len(cells[0].text) == 4:
            built = cells[3].text   # YYYY or mm.YYYY
            year = built[-4:]       # drop month if exists
            trams[year] = trams.get(year, 0) + 1

    for year in sorted(trams):
        print(year, trams[year], '#' * trams[year], sep='\t')


if __name__ == '__main__':
    main()
