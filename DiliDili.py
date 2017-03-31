import requests
import lxml
from bs4 import BeautifulSoup

url = 'http://www.dilidili.wang/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}
text = ''
try:
    print('Request url:', url)
    text = requests.get(url, headers=headers, timeout=10)
    text.encoding='utf-8'
except Exception as e:
    print(e)

soup = BeautifulSoup(text.text, 'lxml').find('ul', class_='nav_lef fl').find_all('a')
for a in soup:
    print(a.get_text(),a['href'])


