from urllib import request
import pickle
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def create_list(toFile=True, filename='list', categorize=False):
    """
    creates a simple colon seperated file channelname:integer
    :param toFile: if false return as string else save to filename
    :param filename: name of file to save as
    :param categorize: Categorize output if True else just single file
    :return: string or none
    """

    if toFile:
        file = open(filename, 'w')
    else:
        import io
        file = io.StringIO()

    html = request.urlopen('http://tv.burrp.com/channels.html').read()
    soup = BeautifulSoup(html, 'lxml')

    fieldsets = soup.select('div.main > fieldset')
    for fs in fieldsets:
        if categorize:
            title = fs.legend.string.strip()
            file.write(title+'\n')
        a_lst = fs.find_all('a')
        for a in a_lst:
            array = a['href'].split('/')
            file.write(array[-3]+':'+array[-2]+'\n')
        if categorize:
            file.write('\n\n')

    if toFile:
        file.close()
    else:
        a = file.getvalue()
        file.close()
        return a


def create_dict(toFile=True, filename='list'):
    """
    creates a dictionary from file already saved as colon seperated values.
    dumps the dictionary as filename.dict as pickle
    :param toFile: save data to file if True else return as dict
    :param filename: name of colon sepereated values
    :return:
    """
    if toFile:
        file = open(filename, 'r')
    else:
        import io
        file = io.StringIO(create_list(False))

    line = file.readline()
    dct = {}
    while line:
        a, b = line.strip().split(':', 2)
        dct[a] = int(b)
        line = file.readline()

    file.close()

    if toFile:
        file2 = open(filename+'.dict', 'wb')
        pickle.dump(dct, file2)
        file2.close()
    else:
        return dct

print(create_dict(False))