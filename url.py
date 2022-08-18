from urllib import parse
from urllib import request
from http import cookiejar
from pathlib import Path
from bs4 import BeautifulSoup
from mudules import download
import ssl
import gzip


ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.sui.com/data/index.jsp'

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
    # 'cookie': '__nick=zhhony%40126.com; _bookTabSwitchList=3a36ab85ce6f7073b89800b4195a7882|0|0&; __utmz=121176714.1658384441.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __spm_bid=c0c9bda5865bs9dfp7153cc21fm7689f; SESSION=e6c7faed-e4c7-4a1a-889c-9042eeda3b3b; SESSION_COOKIE=d9e21fbbd853e2d89543561dfe485965; Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4=1658384437,1659581002,1660552239,1660612833; __utma=121176714.1216454833.1658384441.1660552239.1660612833.5; __utmc=121176714; __utmt=1; Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4=1660612836; __utmb=121176714.3.9.1660612836172',
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
    cookieFileList = [i for i in path.iterdir() if 'Cookie' in str(i)]
    cookieFileList.sort()
    return str(cookieFileList[-1])


lastCookie = latestDocument('./log/')
cookie_jar = cookiejar.MozillaCookieJar(lastCookie)
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = request.HTTPCookieProcessor(cookie_jar)
opener = request.build_opener(cookie_processor)

req = request.Request(url, headers=headers, method='GET')
response = opener.open(req)
html = gzip.decompress(response.read()).decode('utf8')


soup = BeautifulSoup(html)
downloadPath = soup.find_all(
    'a', onclick="_gaq.push(['_trackEvent', 'webExport', 'clicked'])")[0]['href']
downloadUrl = parse.urljoin(url, downloadPath)


# requestA = request.Request(url=downloadUrl, headers=headers, method='GET')
# file = opener.open(requestA)
# dict(file.headers)


download.Downunit(url=downloadUrl, path='./data/abc.xls',
                  opener=opener, headers=headers).Download()
