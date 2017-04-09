import requests
import lxml
from bs4 import BeautifulSoup
import crawlDilidili

def getAllSetUrl(comicTuple):
    url = str(comicTuple[1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    try:
        print('Request url:', url)
        text = requests.get(url, headers=headers, timeout=10)
        text.encoding = 'utf-8'
    except Exception as e:
        print(e)
    comicSetList = []

    try:
        soup = BeautifulSoup(text.text, 'lxml').find('ul', class_='clear').find_all('a')
    except Exception as e:
        print(e)
        return None
    try:
        for set in soup:
            comicSetDict = {'name': None,
                            'set': None,
                            'setinfo': None,
                            'seturl': None,
                            'comicurl': None}
            comicSetDict['name'] = str(comicTuple[0])
            comicSetDict['set'] = set.find('span').get_text()
            comicSetDict['setinfo'] = set.get_text().split()[len(set.get_text().split()) - 1]
            comicSetDict['seturl'] = set['href']
            comicSetDict['comicurl'] = url
            comicSetList.append(comicSetDict)
    except Exception as e:
        print(e)
        return None
    #print(comicSetList)
    return comicSetList