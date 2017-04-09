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
    soup = BeautifulSoup(text.text, 'lxml').find('div', class_='zmfl').find_all('li')
    for li in soup:
        #print(li)
        tempDict = {
            'title': None,
            'url': None}
        tempDict['title'] = li.get_text()
        tempDict['url'] = li.find('a')['href']
        comicList.append(tempDict)
    return comicList