import requests
import lxml
from bs4 import BeautifulSoup


def getComicInfoFromUrl():
    url = 'http://www.dilidili.wang/kehuan/'
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
                         'curl': None,
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
        #print(len(str(dd.find('a')['href'])), len('http://www.dilidili.wang'))
        if len(str(dd.find('a')['href'])) > len('http://www.dilidili.wang'):
            comicInfoDict['curl'] = str(dd.find('a')['href'])
        else:
            comicInfoDict['curl'] = 'http://www.dilidili.wang' + str(dd.find('a')['href'])
        for b in dd.find_all('div', class_='d_label'):
            if b.get_text().split('：')[0] == '地区':
                comicInfoDict['area'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '年代':
                comicInfoDict['publishtime'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '标签':
                comicInfoDict['label'] = b.get_text().split('：')[1]
            if b.get_text().split('：')[0] == '播放':
                if b.get_text().split('：')[1] == '':
                    comicInfoDict['playedtime'] = None
                else:
                    comicInfoDict['playedtime'] = b.get_text().split('：')[1]
        for p in dd.find_all('p'):
            #print(p.get_text().split(':'))
            if p.get_text().split(':')[0] == '状态':
                comicInfoDict['state'] = p.get_text().split(':')[1]
            if p.get_text().split('：')[0] == '看点':
                comicInfoDict['focus'] = p.get_text().split('：')[1][:100]
            if p.get_text().split('：')[0] == '简介':
                comicInfoDict['summary'] = p.get_text().split('：')[1][:100]
        #comicInfoDict['belone'] = comicDict['title']
        comicInfoList.append(comicInfoDict)
    for cm in comicInfoList:
        print(cm)
    #return comicInfoList


getComicInfoFromUrl()