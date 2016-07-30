# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import cookielib
import re

login_url = 'https://cas.xjtu.edu.cn/login?service=http://ssfw.xjtu.edu.cn/index.portal'

ua = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding' : 'gzip, deflate, sdch, br',
	'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
	'Connection' : 'keep-alive',
	'DNT' : '1',
	'Host' : 'cas.xjtu.edu.cn',
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

class Cas():
	def __init__(self, usr, psw):
		self.usr = usr
		self.psw = psw

		self.cookie = cookielib.MozillaCookieJar()
		self.cookie.load(usr, ignore_discard=True, ignore_expires=True)
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

		self.link = None
		result = self.old_cookie_login()
		if not result:
			self.login()
		if self.link and len(self.link) != 0:
			result = self.opener.open(self.link[0])
			self.cookie.save(usr, ignore_discard=True, ignore_expires=True)
			print 'Login Success!'


	def is_success(self, html):
		pattern = re.compile(r'<title>(.+?)</title>', re.S)
		title = re.findall(pattern, html)
		if len(title) == 1 and title[0] == '\xe7\xbb\x9f\xe4\xb8\x80\xe8\xba\xab\xe4\xbb\xbd\xe8\xae\xa4\xe8\xaf\x81\xe7\xbd\x91\xe5\x85\xb3':
			return False
		return True

	def old_cookie_login(self):
		result = self.opener.open(login_url)
		html = result.read()
		if self.is_success(html):
			self.link = self.get_link(html)
			print 'Old cookie vaild.'
			return True
		else:
			print 'Old cookie invaild.'
			return False

	def login(self):
		result = self.opener.open(login_url)
		html = result.read()
		lt, exe = self.get_keys(html)

		postdata = urllib.urlencode({
			'username' : self.usr,
			'password' : self.psw,
			'lt' : lt,
			'execution' : exe,
			'_eventId' : 'submit'
		})

		request = urllib2.Request(
			url = login_url,
			data = postdata,
			headers = ua
		)

		result = self.opener.open(request)
		html = result.read()
		self.link = self.get_link(html)


	def get_link(self, html):
		pattern = re.compile(r'url=(.+?)"/>', re.S)
		return re.findall(pattern, html)


	def get_keys(self, html):
		pattern = re.compile(r'type="hidden".+value="(.+?)"')
		keys = re.findall(pattern, html)
		return keys[0], keys[1]


if __name__ == '__main__':
	usr = sys.argv[1]
	psw = sys.argv[2]
	cas = Cas(usr, psw)
	if cas.link and len(cas.link) != 0:
		result = cas.opener.open(cas.link[0])
		print result.read()