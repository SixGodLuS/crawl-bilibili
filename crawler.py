import requests
import json
from datetime import datetime, timedelta
import re

def crawlBiliBili():
    url = 'http://space.bilibili.com/562197/#!/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }  # headers这一段不需要改动
    text = ''
    try:
        print('Requesting url: ', url)
        text = requests.get(url, headers=headers, timeout=10).text
    except:
        print('Error when request url=', url)
        return None
    print(text)
    pass
crawlBiliBili()