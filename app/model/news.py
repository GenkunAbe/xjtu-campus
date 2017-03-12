# -*- coding: utf-8 -*-

from model.cas import Cas
import re
import urllib.request
import urllib
import json
import http.cookiejar
import requests

urls = {
  'xytz' : 'http://dean.xjtu.edu.cn/jxxx/xytz.htm',
  'zhtz' : 'http://dean.xjtu.edu.cn/jxxx/zhtz.htm',
}

class News:

  def __init__(self):
    self.s = requests.Session()

  def get_list(self, url, index=1):
    uri = url
    result = self.s.get(uri)
    result.encoding = "utf-8"
    html = result.text

    pattern = re.compile(r'list_time">(.+?)</span>.+?style="float:left".+?href="(.+?)" target="_blank" title="(.+?)".*?>', re.S)
    lines = re.findall(pattern, html)

    return lines

  def ez_get(self):
    return self.get_list(urls['xytz'], 1) + self.get_list(urls['zhtz'], 1)



if __name__ == '__main__':
  news = News()
  lines = news.ez_get()
  for line in lines:
    print(line[0], line[1], line[2])