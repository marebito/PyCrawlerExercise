#!/usr/local/bin/python3

'樊登读书会爬虫'

__author__ = 'Yuri Boyka'

from bs4 import BeautifulSoup
import urllib3
import requests
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "http://dushu.fandengds.com/cy/index.html"


def parseContent(content):
    # BeautifulSoup解析
    soup = BeautifulSoup(content, "lxml")
    target = soup.find(name="div", attrs={'class': {"book_ls"}})
    li_list = target.find_all('li')
    for li in li_list:
        a_tag = li.find('a')
        if a_tag:
            href = "http://dushu.fandengds.com" + a_tag.attrs.get("href")
            title = a_tag.attrs.get("title")
            book_cover = "http://dushu.fandengds.com" + \
                a_tag.find("img").attrs.get('src')
            book_name = a_tag.find("div", class_="bkname text-nowrap")
            book_author = a_tag.find("div", class_="bkauthor text-nowrap")
            book_intro = a_tag.find("div", class_="bkintro text-nowrap")
            print("[书名]: "+book_name.text+"\n[作者]: " +
                  book_author.text+"\n[简介]: "+book_intro.text + "\n[链接]: " + href + "\n[封面]: " + book_cover + "\n[标题]: "+title + "\n")


def requestUrl(scrapy_url):
    # 获取数据
    response = requests.get(url)
    # 获取数据编码
    print("[编码]: "+response.encoding + "\n[状态码]:" +
          str(response.status_code) + "\n[内容]:\n" + response.text)
    # 将数据编码成utf-8编码
    response.encoding = 'utf-8'
    parseContent(response.text)


def urllib3Request(scrapy_url):
    # 一个PoolManager实例来生成请求, 由该实例对象处理与线程池的连接以及线程安全的所有细节
    http = urllib3.PoolManager()
    # 通过request()方法创建一个请求：
    response = http.request('GET', scrapy_url)
    print("[状态码]: "+str(response.status) + "\n[数据]: \n"+response.data.decode())
    parseContent(response.data.decode())


if __name__ == "__main__":
    urllib3Request(url)
