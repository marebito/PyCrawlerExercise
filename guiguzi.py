#!/usr/local/bin/python3

'鬼谷子全译本爬虫'

__author__ = 'Yuri Boyka'

from bs4 import BeautifulSoup
import requests
import io
import sys
from sqlalchemy import create_engine

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_catalog(catalog_url):
    response = requests.get(catalog_url)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'lxml')
    target = soup.find(name='div', attrs={'class': {'gushilist'}})
    li_list = target.find_all('li')
    for idx, li in enumerate(li_list):
        if idx < len(li_list) - 1:
            a_tag = li.find('a')
            if a_tag:
                chapter_name = li.string
                chapters_url = "http://www.skyjiao.com" + a_tag.attrs.get("href")
                print("[章 节] " + chapter_name + "\n[链 接] " + chapters_url)
                chapters = get_chapters(chapters_url)
                if chapters:
                    for chapter_info in chapters:
                        for chapter in chapter_info:
                            chapter_content = get_chapter_content(chapter_info[chapter])
                        print(chapter_content)


def get_chapters(chapters_url):
    response = requests.get(chapters_url)
    response.encoding = "gb2312"
    soup = BeautifulSoup(response.text, 'lxml')
    page_list = soup.find(name="ul", attrs={'class': {'pagelist'}})
    chapter_info = []
    if page_list:
        pages = page_list.find_all('li')
        if pages:
            for idx, page in enumerate(pages):
                ch_url = ''
                if idx >= 2 and idx < len(pages) - 1:
                    if idx == 2:
                        ch_url = chapters_url
                    if idx > 2:
                        ch_url = "http://www.skyjiao.com/guwen/" + (page.find("a")).attrs.get('href')
                    chapter = {}
                    chapter[idx - 1] = ch_url
                    chapter_info.append(chapter)
            return chapter_info
        else:
            chapter_info.append({'1': chapters_url})
    return chapter_info


def get_chapter_content(chapter_url):
    response = requests.get(chapter_url)
    response.encoding = "gb2312"
    soup = BeautifulSoup(response.text, 'lxml')
    target = soup.find(name='div', attrs={'class': {'text'}})
    div_list = target.find_all(name='div')
    for div in div_list:
        div.decompose()
    target.p.decompose()
    return target.text


if __name__ == '__main__':
    get_catalog("http://www.skyjiao.com/guwen/guiguzi/")
