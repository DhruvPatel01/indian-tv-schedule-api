"""
this module contains main functions to parse web pages given url
"""

from datetime import date

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import json
import pickle

try:
    from urllib import quote as url_quote
except ImportError:
    from urllib.parse import quote as url_quote

def _to_camel_case(str):
    if str[-1] == ':':
        lst = str[:-1].split(' ')
    else:
        lst  = str.split(' ')
    return lst[0].lower() + ''.join([a.title() for a in lst[1:]])

def  _tr_limiter(tr):
    """check if first td has class resultTime
    if yes return True
    """
    if tr.td and 'resultTime' in tr.td['class']:
        return True
    else:
        return False


def _update_table(table):
    """
    updates the table if table contains schedule of two days \
    happens when date is today's
    :param table: table tag to update
    :return: none
    """

    lst = table.find_all('td', {'class': 'dateHdr'})
    if len(lst) == 1:
        return
    lst[0].extract()
    tr = lst[1].parent
    while tr.next_sibling:
        tr.next_sibling.extract()
    tr.extract()

def parse_show_page(url, show_meta=True, show_details=False, json_out=False, indent=None):
    """
    parses and returns about show as dictionary or json
    :param url: url of the page to parse
    :param show_meta: meta data about show like showType, language, drama
    :param show_details: details about the show
    :param json_out: output as json if True as list
    :return: output as json or dictionary indexed by meta and details
    """
    out = {}
    html = urlopen(url).read()
    if not show_details:
        strainer = SoupStrainer('td', {'class':['showDetails']})
    else:
        strainer = SoupStrainer('body')
    soup = BeautifulSoup(html, 'lxml', parse_only=strainer)

    if show_meta:
        table = soup.select('td.showDetails > table')
        dct = {}
        tr = table[0].tr
        tr.extract()
        tr_lst = table[0].find_all('tr')
        for tr in tr_lst:
            th = tr.th
            if th:
                dct[_to_camel_case(th.string.strip())] = tr.td.string.strip()
        out['meta'] = dct

    if show_details:
        dct = {}
        synopsis = soup.select('div.synopsis')
        if synopsis:
            dct['showDescription'] = synopsis[0].get_text().strip()
            table = synopsis[0].parent.find('table', class_='meta')
        else:
            table = None
            dct['showDescription'] = 'No Description'

        if table:
            tr_lst = table.find_all('tr')
            for tr in tr_lst:
                th = tr.th
                if th:
                    dct[_to_camel_case(th.string.strip())] = tr.td.get_text().strip()

        if dct:
            out['details'] = dct

    if json_out:
        return json.dumps(out, sort_keys=True, indent=indent)
    else:
        return out


def parse_channel_page(url, show_meta=True, show_details=False, json_out=False, indent=None):
    """
    parses and returns show list of channel page
    :param url: url of the page to parse
    :param show_meta: meta data about show like showType, language, drama
    :param show_details: details about the show
    :param json_out: output as Json string if True else dictionary
    :param indent: +ve value to prettify output json
    :return: json string or dictionary
    """
    html = urlopen(url).read()

    strainer = SoupStrainer('table', {'class':'result'})
    table = BeautifulSoup(html,'lxml', parse_only=strainer)
    _update_table(table)

    tr_list = filter(_tr_limiter, table.find_all('tr'))
    show_list = {}
    show_list['shows']= []
    meta = {}#hashtable to avoid reparsing
    details = {}#hashtable to avoid reparsing
    for tr in tr_list:
        td_list = tr.find_all('td')
        dct = {}
        h, m = td_list[0].b.contents[0].strip().split(':', 2)
        h,m = int(h), int(m)
        if td_list[0].b.sup.string.lower() == 'pm' and h != 12:
            h += 12
        dct['showTime'] = "{0:02}:{1:02}".format(h, m)
        dct['showTitle'] = ' '.join(td_list[2].a.get_text().strip().split())
        dct['showThumb'] = td_list[1].a.img['src']

        if show_meta or show_details:
            shm = show_meta
            shd = show_details
            if show_meta and dct['showTitle'] in meta:
                dct.update(meta[dct['showTitle']])
                shm = False
            if show_details and dct['showTitle'] in details:
                dct.update(details[dct['showTitle']])
                shd = False
            if shm or shd:
                show_url = url_quote(td_list[2].a['href'], '/:')
                meta_details = parse_show_page(show_url, show_meta, show_details)
                if shm:
                    dct.update(meta_details['meta'])
                    meta[dct['showTitle']] = meta_details['meta']
                if shd:
                    dct.update(meta_details['details'])
                    details[dct['showTitle']] = meta_details['details']
        show_list['shows'].append(dct)

    if json_out:
        return json.dumps(show_list,sort_keys=True, indent=indent, ensure_ascii=False)
    else:
        return show_list

def get_show_list(channel, date=date.today(), show_meta=False, show_details=False, indent=None):
    """
    returns json string of shows for channel if wrong channel name returns False
    :param channel: name of the channel
    :param date: date of the schedule
    :param show_meta: also include meta data if True
    :param show_details: also include show details if True
    :param indent: +ve no. specifies the number of spaces to prettify output
    :return:json string on success, False on error
    """

    try:
        f = open('list.dict', 'rb')
        dct = pickle.load(f)
        f.close()
    except:
        import channel_list_parser
        dct = channel_list_parser.create_dict(False)

    if channel not in dct:
        return False

    url = "http://tv.burrp.com/channel/{0}/{1!s}/{2}%2000:00:00".format(channel, dct[channel],date.strftime('%Y-%m-%d'))
    show_list = parse_channel_page(url, show_meta, show_details)
    show_list['date'] = date.strftime('%Y-%m-%d')
    show_list['channel'] = channel
    return json.dumps(show_list, sort_keys=True, indent=indent, ensure_ascii=False)

if __name__ == '__main__':
    print(get_show_list('star-movies', indent=4))