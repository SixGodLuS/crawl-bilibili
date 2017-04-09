import requests
import lxml
from bs4 import BeautifulSoup

def getNeedUrl():
    url = 'http://www.dilidili.wang/a/'
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
    comicList = []
    soup = BeautifulSoup(text.text, 'lxml').find_all('div', class_='tagbox')
    for nf in soup:
        for li in nf.find_all('div', class_='nianfan'):
            for a in li.find_all('a'):
                tempDict = {
                    'title': None,
                    'url': None}
                #print(a.get_text())
                if (a.get_text() == '日本'
                    or a.get_text() == '中国'
                    or a.get_text() == '欧美'
                    or a.get_text() == '港台'):
                    tempDict['title'] = a.get_text()
                    tempDict['url'] = a['href']
                    comicList.append(tempDict)
    for li in comicList:
        print(li)
    return comicList
