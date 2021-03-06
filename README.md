# Compute age of trams in Russian cities

The most of systems of public transportation in Russia uses ancient wagons.
List of passenger vehicles by particular city is available at URL like https://transphoto.org/list.php?serv=0&cid=54&t=1, list of Russian cities available at https://transphoto.org/country/1/

This program fetches data for specified city and type of transportation and then make some statistical computation.

## Preparing

```bash
make prepare
. env/bin/activate
```

or

```bash
sudo apt install pip3-venv
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
compute.py [-h] [-c CITY] [-t TYPE] [-l LANGUAGE]
```

### Optional arguments

* `-h`, `--help` — show help message and exit
* `-c` _CITY_, `--city` _CITY_ — number or name
   (default city is Moscow)
* `-t` _TYPE_, `--type` _TYPE_ — transportation type
   (digit `1` to `9` or name, default value is tram)
* `-l` _CODE_, `--language` _CODE_ —
   [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1)
   language code (default is `ru` for Russian)
* `-o` _FILE_, `--output` _FILE_ — output frequency table to file.
   Format detected by filename without case sensitivity.

#### File formats

* CSV — Comma Separated Values — `file.csv`
* HTML — Hypertext Markup Language — `file.htm`, `file.html`
* JSON — JavaScript Notation Object — `file.json`, `file.js`
* Microsoft Excel — `file.xls` (legacy), `file.xlsx`


## Examples

It's possible to use digital IDs

```
$ python compute.py --city 229 --type 2
Миасс, троллейбус
-----------------
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
Total     28
Mean: 2002.6, median: 2006.5, modes: [2009]
```

or human readable names

```
$ python compute.py --city Ekb --type metro --language en
Yekaterinburg, metro
--------------------
1988       6 ######
1989      39 #######################################
2011       8 ########
2019       8 ########
------------
Total     61
Mean: 1995.7, median: 1989.0, modes: [1989]
```

Names can be specified in English or in Russian.
There are aliases for cities and types for example:
* metro = metropolitain = subway = underground
* tramway = tram = tm
* SPb = Saint Petersburg = Petersburg

## See also

* https://transphoto.org/country/1/
* https://www.facebook.com/chelurban/posts/927689021093721
* http://shoorick.ru/2017/11/10/old-trams/

## Author

Alexander Sapozhnikov
http://shoorick.ru/
<shoorick@cpan.org>
