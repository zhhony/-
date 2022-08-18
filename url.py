from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
from pathlib import Path
import time
import ssl
import gzip
import os
import re
import pandas
from bs4 import *

pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.sui.com/data/standard_data_import.do?m=exportAll&bids=0&sids=0&pids=0&token=31a88f6cd6b822e5c3f244eb6d1637af'

# request模块
headers = {
    'authority': 'www.sui.com',
    'method': 'GET',
    'path': '/data/index.jsp',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '__nick=zhhony%40126.com; _bookTabSwitchList=3a36ab85ce6f7073b89800b4195a7882|0|0&; __utmz=121176714.1658384441.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __spm_bid=c0c9bda5865bs9dfp7153cc21fm7689f; SESSION=e6c7faed-e4c7-4a1a-889c-9042eeda3b3b; SESSION_COOKIE=d9e21fbbd853e2d89543561dfe485965; Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4=1658384437,1659581002,1660552239,1660612833; __utma=121176714.1216454833.1658384441.1660552239.1660612833.5; __utmc=121176714; __utmt=1; Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4=1660612836; __utmb=121176714.3.9.1660612836172',
    'pragma': 'no-cache',
    'Referer': 'https://www.sui.com/report_index.do',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'Upgrade-Insecure-Requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def latestDocument(cookiePath: str) -> str:
    path = Path(cookiePath)
    cookieFileList = [i for i in path.iterdir() if 'cookie' in str(i)]
    cookieFileList.sort()
    return str(cookieFileList[-1])


lastCookie = latestDocument('./log/')
cookie_jar = MozillaCookieJar(lastCookie)
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)

request = Request(url, headers=headers, method='GET')
response = opener.open(request)
html = response.read()


with open('./data/abc.xls', 'wb') as f:
    f.write(html)
