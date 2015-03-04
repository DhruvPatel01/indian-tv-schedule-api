#Dependencies#
+ Python 3
+ bs4 (BeautifulSoup4)
To install it use `pip install bs4`

#Usage#

`python3 main.py [-h] [--create] [-c CHANNEL] [-d DATE] [-m] [-D] [-i INDENT]`

##optional arguments:

`-h`, `--help`
show this help message and exit

`--create`
Create the list of channels available

`-c CHANNEL`, `--channel CHANNEL`
Show the schedule for this channel

`-d DATE`, `--date DATE`
Schedule for this date. format YYYY-MM-DD. defaults to today.

`-m`, `--meta`
Include meta data of show like genre,language, type in output.

`-D`, `--details`         Include extra details of show in output.

`-i INDENT`, `--indent INDENT`
Prettify output json with i indents. use -1 to compact
