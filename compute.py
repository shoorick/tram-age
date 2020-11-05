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

    table = soup.find('table', {'class': 'p20w'})
    if not table:
        sys.exit("Can't find table")

    rows = table.find_all('tr')
    for row in rows:
        cells = rows.find('td')
        print(cells)


if __name__ == '__main__':
    main()
