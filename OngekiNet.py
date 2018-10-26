import sys, os

import urllib.request
from urllib.parse import urlencode
import http.cookiejar
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class OngekiNet:
    def __init__(self):
        pass


    def login(self, name, password):

        self.cookiefile = "cookies.txt"
        self.cj = http.cookiejar.LWPCookieJar()
        if os.path.exists(self.cookiefile):
            self.cj.load(self.cookiefile)

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(opener)

        top_url    = 'https://ongeki-net.com/ongeki-mobile/'
        submit_url = 'https://ongeki-net.com/ongeki-mobile/submit/'

        headers1 = {
            "Accept" :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding" :"gzip, deflate, br",
            "Accept-Language" :"ja,en-US;q=0.8,en;q=0.6",
            "Cache-Control" :"max-age=0",
            "Connection" :"keep-alive",
            "Content-Type" :"application/x-www-form-urlencoded"
        }

        # ログインする際にtokenが必要になるためtop画面よりいただく
        req = urllib.request.Request(top_url, None, headers1)
        with urllib.request.urlopen(req) as res:
            html = res.read().decode("utf-8")
            cookie = res.getheader('Set-Cookie')
            res.close()

        soup = BeautifulSoup(html, "html.parser")
        token = soup.find(attrs={'name': 'token'}).get('value')
        cookie = cookie + '; segaId=' + name

        headers2 = {
            "Accept" :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding" :"gzip, deflate, br",
            "Accept-Language" :"ja,en-US;q=0.9,en;q=0.8",
            "Cache-Control" :"max-age=0",
            "Connection" :"keep-alive",
            "Content-Length" : "96",
            "Content-Type" :"application/x-www-form-urlencoded",
            "Host": 'ongeki-net.com',
            "Origin": 'https://ongeki-net.com',
            "Referer" : 'https://ongeki-net.com/ongeki-mobile/',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

        login_post = {
            'segaId': name,
            'password': password,
            'save_cookie': "on",
            'token': token
        }

        data = urllib.parse.urlencode(login_post).encode("utf-8")

        req = urllib.request.Request(submit_url, None, headers2)
        with urllib.request.urlopen(req, data=data) as res:
            html = res.read().decode("utf-8")
            res.close()

        print (html)

if __name__ == '__main__':
    args = sys.argv
    on = OngekiNet()

    on.login(args[1], args[2])
