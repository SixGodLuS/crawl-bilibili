import requests
import lxml
from bs4 import BeautifulSoup
import mysql.connector
import crawlComicInfoByTag
import  crawlComicInfoByArea
import crawlComicAllSet
import crawlComicByLibrary

DBCONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'port':3306,
    'database': 'databasefordilidili',
    'charset': 'utf8'
}
conn = mysql.connector.connect(**DBCONFIG)
cursor = conn.cursor()

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
    url = str(comicDict['url'])
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
        #print(str(dd.find('a')['href'])[:1])
        if str(dd.find('a')['href'])[:1] == '/':
            comicInfoDict['curl'] = 'http://www.dilidili.wang' + str(dd.find('a')['href'])
        else:
            comicInfoDict['curl'] = str(dd.find('a')['href'])
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
    return comicInfoList
def savecomicSummaryIntoDatabase(comicInfoDict):
    print('Saving comic #', comicInfoDict['name'], 'into db')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    conn.commit()
    try:
        cursor.execute(
            'replace into comic_information'
        '(Name, ComicUrl, Area, PublishTime, Label, PlayedTime, Focus, Summary, State)'
        'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        [comicInfoDict['name'], comicInfoDict['curl'], comicInfoDict['area'],
         comicInfoDict['publishtime'], comicInfoDict['label'], comicInfoDict['playedtime'],
         comicInfoDict['focus'], comicInfoDict['summary'], comicInfoDict['state']])
        conn.commit()
    except Exception as e:
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def savecomicSetIntoDatabase(setDict):
    print('Saving comic #', setDict['name'], setDict['set'], 'into db')
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    conn.commit()
    try:
        cursor.execute(
            'replace into comic_information'
        '(Name, Set, SetInfo, SetUrl, ComicUrl'
        'values(%s, %s, %s, %s, %s)',
        [setDict['name'], setDict['set'], setDict['setinfo'], setDict['seturl'], setDict['comicurl']])
        conn.commit()
    except Exception as e:
        print(e)
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')  # 重新开启外键检测
    conn.commit()

def getComicInfoFromDB():
    cursor.execute('select * from comic_information')
    return (cursor.fetchall())

def main():
    urlList = []
    urlList.append(crawlComicInfoByTag.getNeedUrl())
    urlList.append(crawlComicByLibrary.getNeedUrl())
    sumComicInfoList = []
    comicSetList = []
    for comicList in urlList:
        for comicDict in comicList:
            sumComicInfoList.append(getComicInfoFromUrl(comicDict))
    sumTuple = getComicInfoFromDB()
    print(len(sumComicInfoList))
    for comicInfoList in sumComicInfoList:
        for comicInfoDict in comicInfoList:
           if sumTuple:
               flag = 0
               for comicTuple in sumTuple:
                   if comicInfoDict['curl'] == comicTuple[1]:
                       flag = 1
                       break
               if flag == 0:
                   print(comicInfoDict)
                   savecomicSummaryIntoDatabase(comicInfoDict)
           else:
               savecomicSummaryIntoDatabase(comicInfoDict)
    #爬取动漫分集url
    if sumTuple:
        for comicTuple in sumTuple:
            comicSetList.append(crawlComicAllSet.getAllSetUrl(comicTuple))
        for setDict in comicSetList:
            print(setDict)
            savecomicSetIntoDatabase(setDict)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()