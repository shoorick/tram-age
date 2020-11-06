# Compute age of trams in Chelyabinsk

Chelyabinsk is a big Russian city having large tram network (68 km) but the most of tram wagons are ancient.
List of passenger vehicles is available at https://transphoto.org/list.php?serv=0&cid=54&mid=1

This program fetches data from specified web page and then make some statistical computation.

## Preparing

```bash
sudo apt install pip3-venv
python3 -m venv env
. env/bin/activate
pip install lxml bs4
```

## Sample of output

```
$ python compute.py --city Miass --type 2
Миасс, троллейбус
-----------------
           3 ###
1987       1 #
1988       3 ###
1989       1 #
1992       2 ##
1993       2 ##
2002       2 ##
2004       1 #
2005       1 #
2006       1 #
2007       1 #
2008       3 ###
2009       6 ######
2011       1 #
2020       2 ##
------------
Total     30
```

## See also

* https://transphoto.org/country/1/
* https://www.facebook.com/chelurban/posts/927689021093721
* http://shoorick.ru/2017/11/10/old-trams/

## Author

Alexander Sapozhnikov
http://shoorick.ru/
<shoorick@cpan.org>
