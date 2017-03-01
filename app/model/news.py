# -*- coding: utf-8 -*-

from cas import Cas
import re
import urllib.request
import urllib
import json
import http.cookiejar

urls = {
  'xytz' : 'http://dean.xjtu.edu.cn/html/jxxx/xytz/%d.html',
  'zhtz' : 'http://dean.xjtu.edu.cn/html/jxxx/zhtz/%d.html',
}

class News:

  def __init__(self):
    self.cookie = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

  def get_list(self, url, index=1):
    uri = url % index
    result = self.opener.open(uri)
    html = result.read()

    pattern = re.compile(r'<a style="float:left; " href="(.+?)">(.+?)</a>.+?">(.+?)</span>', re.S)
    lines = re.findall(pattern, html)

    for i in range(len(lines)):
      if lines[i][1].startswith('<span'):
        pattern = re.compile(r'>(.+?)<', re.S)
        lines[i] = (lines[i][0], re.findall(pattern, lines[i][1])[0], lines[i][2])

    return lines

  def ez_get(self):
    return self.get_list(urls['xytz'], 1) + self.get_list(urls['zhtz'], 1)



if __name__ == '__main__':
  news = News()
  lines = news.ez_get()
  for line in lines:
    print(line[0], line[1], line[2])