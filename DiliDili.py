import requests
import lxml
from bs4 import BeautifulSoup

def getNeedUrl():
    url = 'http://www.dilidili.wang/'
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
    soup = BeautifulSoup(text.text, 'lxml').find('ul', class_='nav_lef fl').find_all('a')
    for a in soup:
        tempDict = {
            'title': None,
            'url': None}
        print(a.get_text(), a['href'])
        if a.get_text() == '热血动漫':
            tempDict['title'] = a.get_text()
            tempDict['url'] = a['href']
            comicList.append(tempDict)
            break
        else:
            tempDict['title'] = a.get_text()
            tempDict['url'] = a['href']
            comicList.append(tempDict)
    return comicList
def getComicInfoFromUrl(comicDict):
    url = comicDict['url']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    text = ''
    try:
        print('request url:',url)
        text = requests.get(url, headers=headers, timeout=10)
        text.encoding = 'utf-8'
    except Exception as e:
        print(e)
    comicInfoList = []
    soup = BeautifulSoup(text.text, 'lxml').find('div', class_='anime_list').find_all('dd')
    for dd in soup:
        comicInfoDict = {'name': None,
                         'comicurl': 'http://www.dilidili.wang/',
                         'area': None,
                         'publishtime': None,
                         'label': None,
                         'playedtime': None,
                         'focus': None,
                         'summary': None,
                         'state': None,
                         'belone': None}
        #print(dd.find('a'),dd.find_all('div', class_='d_label'),dd.find_all('p'))
        comicInfoDict['name'] = dd.find('a').get_text()
        comicInfoDict['comicurl'] = comicInfoDict['comicurl'] + str(dd.find('a')['href'])
        for b in dd.find_all('div', class_='d_label'):
            if b.get_text().split('：')[0] == '地区':
                comicInfoDict['area'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '年代':
                comicInfoDict['publishtime'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '标签':
                comicInfoDict['label'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '播放':
                comicInfoDict['playedtime'] = b.get_text().split('：')[1]
        for p in dd.find_all('p'):
            #print(p.get_text().split(':'))
            if p.get_text().split(':')[0] == '状态':
                comicInfoDict['state'] = p.get_text().split(':')[1]
            if p.get_text().split('：')[0] == '看点':
                comicInfoDict['focus'] = p.get_text().split('：')[1]
            if p.get_text().split('：')[0] == '简介':
                comicInfoDict['summary'] = p.get_text().split('：')[1]
        comicInfoDict['belone'] = comicDict['title']
        comicInfoList.append(comicInfoDict)
    return comicInfoList

def main():
    urlList = getNeedUrl()
    sumComicInfoList = []
    for comicDict in urlList:
        sumComicInfoList.append(getComicInfoFromUrl(comicDict))
    for comicInfoList in sumComicInfoList:
        for comicinfoDict in comicInfoList:
            print(comicinfoDict)

if __name__ == '__main__':
    main()