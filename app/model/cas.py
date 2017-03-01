# -*- coding: utf-8 -*-

import sys
import urllib
import urllib.request
import http.cookiejar
import re
import os

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

		self.user_dir = "./data/" + usr
		if not os.path.exists(self.user_dir):
			os.mkdir(self.user_dir)
		self.cookie_file_name = self.user_dir + "/cookie"

		is_netid_same = False
		try:
			f = open(self.user_dir + '/netid', 'r')
			lines = f.readlines()
			is_netid_same = (usr == lines[0][0:-1] and psw == lines[1])
		except:
			print("NetId file not exits")

		self.cookie = http.cookiejar.MozillaCookieJar(self.cookie_file_name)
		if not os.path.isfile(self.cookie_file_name) or not is_netid_same:
			self.cookie.save(self.cookie_file_name, ignore_discard=True, ignore_expires=True)
		else:
			self.cookie.load(self.cookie_file_name, ignore_discard=True, ignore_expires=True)
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

		self.link = None
		result = self.old_cookie_login()
		if not result:
			self.login()
		if self.link and len(self.link) != 0:
			result = self.opener.open(self.link[0])
			self.cookie.save(self.cookie_file_name, ignore_discard=True, ignore_expires=True)
			print('Login Success!')
			if not is_netid_same:
				f = open(self.user_dir + '/netid', 'w')
				f.writelines([usr, '\n', psw])

	def load_cookie(self):
		self.cookie.load(self.cookie_file_name, ignore_discard=True, ignore_expires=True)

	def save_cookie(self):
		self.cookie.save(self.cookie_file_name, ignore_discard=True, ignore_expires=True)


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
			print('Old cookie vaild.')
			return True
		else:
			print('Old cookie invaild.')
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

		request = urllib.request.Request(
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
		print(result.read())