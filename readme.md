#Dependencies
+ Python 2 or 3
+ bs4 (BeautifulSoup4)
  + To install it use `pip install bs4`
+ python-lxml, libxml2
  + if you face problem downloding lxml replace `lxml` with `html.parser` in source code.
+ werkzeug (if you want to use it as server)

#Usage

`python3 main.py [-h] [--create] [-c CHANNEL] [-d DATE] [-m] [-D] [-i INDENT] [--server]`

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

##Using as server
To use as server use `--server` flag. The default port is 8080.
Specify custom port using `--port PORT`.

To get json output send GET request to `localhost:port` and use same query as you would use in command line.

e.g.

`localhost:8080/?channel=hbo&meta=true&date=2015-05-05&indent=4`

As server defalut value for indent is  `None`, this is done to reduce size of output.

#Warning
This script parses data from third party website. I didn't found copy right notice or usage policy on their website. Using this api in commercial project should be avoided.
