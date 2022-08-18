from urllib import parse
from urllib import request
from http import cookiejar
from pathlib import Path
from bs4 import BeautifulSoup
from mudules import download
import ssl
import gzip
import time


ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'authority': 'www.sui.com',
    'method': 'GET',
    'path': '/data/index.jsp',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
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


def getLatestFiles(path: str, keyword: str) -> str:
    """获取文件列表中升序排序最下面的文件所对应的路径"""
    path = Path(path)
    cookieFileList = [i for i in path.iterdir() if keyword in str(i)]
    cookieFileList.sort()
    return str(cookieFileList[-1])


def getOpenerDir(cookieFile) -> request.OpenerDirector:
    """基于cookie获取OpenerDirector对象"""
    cookie_jar = cookiejar.MozillaCookieJar(cookieFile)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie_processor = request.HTTPCookieProcessor(cookie_jar)
    return request.build_opener(cookie_processor)


def getDownLoadUrl(motherDownLoadUrl: str, opener: request.OpenerDirector) -> str:
    """基于网址和OpenerDirector对象爬取下载链接"""
    req = request.Request(motherDownLoadUrl, headers=headers, method='GET')
    response = opener.open(req)
    try:
        html = gzip.decompress(response.read()).decode('utf8')
    except:
        print('解压出现错误：%s' % response.read())
        raise ValueError

    soup = BeautifulSoup(html, features='html.parser')
    try:
        downloadPath = soup.find_all(
            'a', onclick="_gaq.push(['_trackEvent', 'webExport', 'clicked'])")[0]['href']
        return parse.urljoin(motherDownLoadUrl, downloadPath)
    except:
        print('寻找标签出现错误:%s' % soup.find_all('a'))
        raise ValueError


def run():
    url: str = 'https://www.sui.com/data/index.jsp'

    lastCookie: str = getLatestFiles('./log/', 'Cookie')
    opener: request.OpenerDirector = getOpenerDir(lastCookie)
    downloadUrl: str = getDownLoadUrl(url, opener)

    download.Downunit(url=downloadUrl, path='./data/abc' + str(int(time.time())) + '.xls',
                      opener=opener, headers=headers).Download()
