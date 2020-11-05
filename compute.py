import sys
import re

def check_version():
    major_version = int(re.search('^\d+', sys.version).group(0))
    if major_version < 3:
        sys.exit('Use version 3 at least\n')

def main():
    check_version()
    print('Not yet implemented')

if __name__ == '__main__':
    main()
