import os
import re
import time
import pdfkit
import threading
import requests
import urllib.parse
import urllib.request
from queue import Queue
from bs4 import BeautifulSoup

values = {}

data = urllib.parse.urlencode(values).encode('utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Connection": "keep-alive",
    "Referer": "https://vjudge.net/",
    "Content-Type": "application/json; charset=utf-8"
}

OJ = {
    "POJ": 1,
    "ZOJ": 1,
    "UVALive": 1,
    "SGU": 1,
    "URAL": 1,
    "HUST": 1,
    "SPOJ": 1,
    "HDU": 1,
    "HYSBZ": 1,
    "UVA": 1,
    "CodeForces": 1,
    "Z-Trening": 1,
    "Aizu": 1,
    "LightOJ": 1,
    "UESTC": 1,
    "UESTC_old": 1,
    "NBUT": 1,
    "FZU": 1,
    "CSU": 1,
    "SCU": 1,
    "ACdream": 1,
    "CodeChef": 1,
    "Gym": 1,
    "OpenJudge": 1,
    "Kattis": 1,
    "HihoCoder": 1,
    "HIT": 1,
    "HRBUST": 1,
    "EIJudge": 1,
    "AtCoder": 1,
    "HackerRank": 1,
}

class uvadownloader(threading.Thread):

    def __init__(self, q, path):
        threading.Thread.__init__(self)
        self.q = q              #下载队列
        self.path = path        #当前地址
        self.filename = ""      #当前下载的文件的文件名 方便输出进度
        self.sch = 0            #进度
        self.working = False    #是否正在工作
        self.exitflag = False   #结束标志

    def run(self):

        #def reporthook(blocks, blocksize, total):
        #    self.sch = min(50, int(blocks * blocksize / total * 50))  #计算进度

        def download(url, ojName, proId):
            response = requests.get(url, params=values, headers=headers).content
            soup = BeautifulSoup(response, 'html.parser')
            match = re.compile(r'href\\u003d\\u0027(.+?)\\u0027\\u003e')
            originurl = re.findall(match, response.decode('utf-8'))
            self.filename = ojName + str(proId) + '.pdf'
            fileurl = self.path + '/' + self.filename
            try:
                urllib.request.urlretrieve(originurl[0], fileurl)
            except:
                os.remove(fileurl)                               #删除下载失败的文件
                self.q.put((url, ojName, proId))                 #放回队列
            #print("Problem " + str(self.id) + " Done")

        while not self.exitflag:
            if not self.q.empty():
                links = self.q.get()
                self.working = True
                download(links[0], links[1], links[2])
                self.sch = 0
                self.working = False

class normalDownloader(threading.Thread):

    def __init__(self, q, path):
        threading.Thread.__init__(self)
        self.q = q              #下载队列
        self.path = path        #当前地址
        self.filename = ""      #当前下载的文件的文件名 方便输出进度
        self.sch = 0            #进度
        self.working = False    #是否正在工作
        self.exitflag = False   #结束标志

    def run(self):

        def download(url, ojName, proId):
            self.filename = ojName + str(proId) + '.pdf'
            fileurl = self.path + '/' + self.filename
            try:
                pdfkit.from_url(url, fileurl)
            except Exception as e:
                os.remove(fileurl)                               #删除下载失败的文件
                self.q.put((url, ojName, proId))                 #放回队列
            #print("Problem " + str(proId) + " Done")

        while not self.exitflag:
            if not self.q.empty():
                links = self.q.get()
                self.working = True
                download(links[0], links[1], links[2])
                self.sch = 0
                self.working = False

class spider:

    def __init__(self, idlist, ojName):
        self.path = os.getcwd() + '/' + ojName
        self.maxdownloader = 5
        self.oj = ojName
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.urlQueue = Queue()
        self.idlist = idlist
        self.downlist = list()

    def crawl(self):

        def getDownlist():
            while len(self.idlist) > 0:
                url = "https://vjudge.net/problem/" + self.oj + "-" + str(self.idlist[0])
                response = requests.get(url, params = values, headers = headers).content
                soup = BeautifulSoup(response, 'html.parser')
                originid = soup.find(attrs = {'data-id':True}).attrs['data-id']
                originurl = "https://vjudge.net/problem/description/" + str(originid)
                self.urlQueue.put((originurl, self.oj, self.idlist[0]))
                self.idlist.pop(0)

        self.crawler = threading.Thread(target=getDownlist())         #开辟一个线程获取网址
        self.crawler.start()
        for i in range (self.maxdownloader):
            if self.oj == 'UVA':                                      #uva直接下载PDF文件
                newthread = uvadownloader(self.urlQueue, self.path)
                newthread.start()
                self.downlist.append(newthread)
            else:                                                     #其他的使用html转换pdf
                newthread = normalDownloader(self.urlQueue, self.path)
                newthread.start()
                self.downlist.append(newthread)
        flag = False
        while len(self.idlist) > 0 or not self.urlQueue.empty() or not flag:
            flag = True
            if len(self.idlist) > 0:
                print('remain ' + str(len(self.idlist)) + ' urls to parse...')
            if not self.urlQueue.empty():
                print(str(self.urlQueue.qsize()) + ' problems ready to download...')
            for i in self.downlist:
                if i.working:
                    flag = False
            time.sleep(0.2)

        for i in self.downlist:                                      #下载结束关闭所有线程
            i.exitflag = True

def main():
    _st = time.time()
    problemst = 1000
    problemed = 1049
    ojname = "UVA"
    if ojname not in OJ:
        return print("check you input")
    idlist = list()
    for i in range(problemst, problemed + 1):
        idlist.append(i)
    solve = spider(idlist, ojname)
    solve.crawl()
    print(time.time() - _st)

if __name__ == "__main__":
    main()
