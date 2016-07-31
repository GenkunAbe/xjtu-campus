# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import json

ua = {
	'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

urls = {
	'main' : 'http://innopac.lib.xjtu.edu.cn',
	'query_book' : 'http://innopac.lib.xjtu.edu.cn/search~S3*chx/?'
}

class Library:

	def __init__(self):
		self.cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

	def get_book_list(self, arg, type='t'):
		arg = arg.encode('utf8')
		postdata = urllib.urlencode([
			('searchtype', 't'),
			('searcharg', arg)
		])
		request = urllib2.Request(
			url = urls['query_book'],
			data = postdata,
			headers=ua
		)
		result = self.opener.open(request)
		html = result.read()

		pattern = re.compile(r'<tr.+?class="browseEntry">\s*(.+?)\s*</tr>', re.S)
		lines = re.findall(pattern, html)

		books = []
		for line in lines:
			pattern = re.compile(r'href="(.+?)">(.+?)</a>')
			items = re.findall(pattern, line)
			if len(items) == 1:
				books.append(items[0])

		return books

	def get_book_detail(self, url):
		uri = urls['main'] + url
		result = self.opener.open(uri)
		html = result.read()

		pattern = re.compile(r'<td.+?class="briefCitRow">\s*(.+?)\s*</table>\s*</td>', re.S)
		lines = re.findall(pattern, html)

		detail = []
		for line in lines:
			pattern = re.compile(r'briefcitTitle">.+?href.+?">(.+?)</a>', re.S)
			title = re.findall(pattern, line)[0]

			pattern = re.compile(r'<br />\s*(.+?)<br />\s*(.+?)<br />', re.S)
			author, press = re.findall(pattern, line)[0]

			pattern = re.compile(r'<tr  class="bibItemsEntry">\s*(.+?)</tr>', re.S)
			indexs = re.findall(pattern, line)

			status = []
			for index in indexs:
				pattern = re.compile(r'&nbsp;(.+?)\s*</td>', re.S)
				items = re.findall(pattern, index)

				pattern = re.compile(r'>(.+?)</a>', re.S)
				items[1] = re.findall(pattern, items[1])[0]
				status.append(items)
			detail.append([title, author, press, status])

		return detail


if __name__ == '__main__':
	library = Library()
	books = library.get_book_list('机器学习')

	for book in books:
		# print book[0], book[1]
		detail = library.get_book_detail(book[0])
		for d in detail:
			print d[0]
			print d[1], d[2]
			for dd in d[3]:
				print dd[0], dd[1], dd[2]
			print '\n\n'