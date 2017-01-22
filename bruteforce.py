#-*-coding:utf-8-*-
import os
import re
import time
import pdfkit
import requests
import urllib.parse
import urllib.request
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

class spider:

    def __init__(self, OjName, id):
        self.oj = OjName
        self.id = id

    def getDescriptionUrl(self):
        url = "https://vjudge.net/problem/" + self.oj + "-" + str(self.id)
        try:
            response = requests.get(url, params = values, headers = headers).content
            soup = BeautifulSoup(response, 'html.parser')
            originid = soup.find(attrs = {'data-id':True}).attrs['data-id']
            url = "https://vjudge.net/problem/description/" + str(originid)
            return url
        except requests.HTTPError as e:
            print(e)

    def getfileurl(self):
        filepath = os.getcwd() + '/' + self.oj
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        filename = self.oj + str(self.id) + '.pdf'
        return filepath + '/' + filename

    def directly(self):
        url = self.getDescriptionUrl()
        response = requests.get(url, params = values, headers = headers).content
        soup = BeautifulSoup(response, 'html.parser')
        match = re.compile(r'href\\u003d\\u0027(.+?)\\u0027\\u003e')
        originurl = re.findall(match, response.decode('utf-8'))
        fileurl = self.getfileurl()
        try:
            urllib.request.urlretrieve(originurl[0], fileurl)
        except urllib.request.HTTPError as e:
            print(e)
        print("Problem " + str(self.id) + " Done")

    def undirectly(self):
        url = self.getDescriptionUrl()
        fileurl = self.getfileurl()
        try:
            pdfkit.from_url(url, fileurl)
        except Exception as e:
            print(e)
        print("Problem " + str(self.id) + " Done")

    def run(self):
        if self.oj == "UVA":
            self.directly()
        else:
            self.undirectly()

def main():
    _st = time.time()
    problemst = 1000
    problemed = 1049
    ojname = "UVA"
    if ojname not in OJ:
        return print("check you input")
    for i in range(problemst, problemed + 1):
        t = spider(ojname, i)
        t.run()
    print(time.time() - _st)

if __name__ == "__main__":
    main()
