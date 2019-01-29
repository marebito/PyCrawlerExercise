#!/usr/local/bin/python3

'樊登读书会爬虫'

__author__ = 'Yuri Boyka'

from bs4 import BeautifulSoup
import urllib3
import requests
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# import pymongo
import pymysql
from DBUtils.PooledDB import PooledDB

from dbConnection.MySqlConn import MyPymysqlPool

url = "http://dushu.fandengds.com/cy/index.html"
global mydb
global cursor


def parseContent(content):
    # BeautifulSoup解析
    soup = BeautifulSoup(content, "lxml")
    target = soup.find(name="div", attrs={'class': {"book_ls"}})
    li_list = target.find_all('li')
    books = []
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
            print("[书名]: " + book_name.text + "\n[作者]: " +
                  book_author.text + "\n[简介]: " + book_intro.text + "\n[链接]: " + href + "\n[封面]: " + book_cover + "\n[标题]: " + title + "\n")
            book = {}
            book["title"] = title
            book["author"] = book_author.text
            book["cover"] = book_cover
            book["name"] = book_name.text
            book["intro"] = book_intro.text
            books.append(book)
    # saveToMongoDB(books)
    saveToMySQL(books)
    # updateBookInfo("联盟", "盟联")


def createTable():
    cursor.execute("DROP TABLE IF EXISTS BOOK")
    # 使用预处理语句创建表
    sql = """
    CREATE TABLE BOOK (
         TITLE  CHAR(255) NOT NULL,
         AUTHOR  CHAR(255),
         COVER CHAR(255),
         NAME CHAR(255),
         INTRO CHAR(255) )
    """
    cursor.execute(sql)


def saveToMySQL(books):
    sql = "INSERT INTO BOOK VALUES"
    for idx, book in enumerate(books):
        s = " ('" + book["title"] + "', '" + book["author"] + "', '" + book["cover"] + "', '" + book["name"] + "', '" + \
            book[
                "intro"] + ("')" if ((len(books) - 1) == idx) else "'),")
        sql += s
    try:
        cursor.execute(sql)
        mydb.commit()
    except:
        mydb.rollback()


# MongoDB Operation
def saveToMongoDB(books):
    mycol = mydb["books"]
    mycol.ensure_index([("title", 1)], unique="unique")
    result = mycol.insert_many(books)
    print(result.inserted_ids)


def getAllBooks():
    mycol = mydb["books"]
    for book in mycol.find():
        print(book)


def deleteBook(name):
    mycol = mydb["books"]
    my_query = {"title": name}
    mycol.delete_one(my_query)


def queryBook(name):
    mycol = mydb["books"]
    for x in mycol.find({"title": name}):
        print(x)


def updateBookInfo(old_name, name):
    mycol = mydb["books"]
    myquery = {"title": old_name}
    newvalue = {"$set": {"title": name}}
    mycol.update_one(myquery, newvalue)


def requestUrl(scrapy_url):
    # 获取数据
    response = requests.get(url)
    # 获取数据编码
    print("[编码]: " + response.encoding + "\n[状态码]:" +
          str(response.status_code) + "\n[内容]:\n" + response.text)
    # 将数据编码成utf-8编码
    response.encoding = 'utf-8'
    parseContent(response.text)


def urllib3Request(scrapy_url):
    # 一个PoolManager实例来生成请求, 由该实例对象处理与线程池的连接以及线程安全的所有细节
    http = urllib3.PoolManager()
    # 通过request()方法创建一个请求：
    response = http.request('GET', scrapy_url)
    print("[状态码]: " + str(response.status) + "\n[数据]: \n" + response.data.decode())
    parseContent(response.data.decode())


if __name__ == "__main__":
    # MySQL Operation
    # mydb = pymysql.connect("localhost", "root", "12345678", "fandengds")
    # cursor = mydb.cursor()
    # cursor.execute("SELECT VERSION()")
    # # 使用 fetchone() 方法获取单条数据.
    # data = cursor.fetchone()
    # print("Database version : %s " % data)
    # createTable()

    # MongoDB初始化
    # myclient = pymongo.MongoClient("mongodb://localhost:27017")
    # mydb = myclient["fandengds"]

    mysql = MyPymysqlPool("db")
    data = mysql.getAll("select *from fandengds.book")
    print(__pool)
    urllib3Request(url)
