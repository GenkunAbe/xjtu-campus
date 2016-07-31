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

	def get_book_detail(self, url, ff=None):
		uri = urls['main'] + url + (('&FF=' + ff) if not ff == None else '')
		uri = uri.replace(' ', '%20')
		result = self.opener.open(uri)
		html = result.read()

		pattern = re.compile(r'<td.+?class="briefCitRow">\s*(.+?)\s*</table>\s*</td>', re.S)
		lines = re.findall(pattern, html)

		detail = []
		if not len(lines) == 0:
			for line in lines:
				pattern = re.compile(r'briefcitTitle">.+?href.+?">(.+?)</a>', re.S)
				title = re.findall(pattern, line)[0]

				pattern = re.compile(r'<br />\s*(.+?)<br />\s*(.+?)<br />', re.S)
				author, press = re.findall(pattern, line)[0]

				status = self.status_parser(line)
				detail.append([title, author, press, status])
		else:
			pattern = re.compile(r'<!-- next row for fieldtag=a -->(.+?)<!-- next row for fieldtag=t -->(.+?)<!-- next row for fieldtag=p -->(.+?)<!-- END INNER BIB TABLE -->', re.S)
			author, title, press = re.findall(pattern, html)[0]

			pattern = re.compile(r'href.+?">(.+?)</a>', re.S)
			author = re.findall(pattern, author)[0]
			press = re.findall(pattern, press)[0]

			pattern = re.compile(r'<strong>(.+?)</strong>', re.S)
			title = re.findall(pattern, title)[0]

			status = self.status_parser(html)
			status = status[0:len(status) / 2]
			detail.append([title, author, press, status])

		return detail

	def status_parser(self, html):
		pattern = re.compile(r'<tr  class="bibItemsEntry">\s*(.+?)</tr>', re.S)
		indexs = re.findall(pattern, html)

		status = []
		for index in indexs:
			pattern = re.compile(r'&nbsp;(.+?)\s*</td>', re.S)
			items = re.findall(pattern, index)

			pattern = re.compile(r'>(.+?)</a>', re.S)
			items[1] = re.findall(pattern, items[1])[0]
			status.append(items)

		return status


if __name__ == '__main__':
	library = Library()
	books = library.get_book_list('机器学习'.decode('utf8'))

	detail = library.get_book_detail(books[1][0])
	for d in detail:
		print d[0]
		print d[1], d[2]
		for dd in d[3]:
			print dd[0], dd[1], dd[2]
		print '\n\n'

	exit()

	for book in books:
		print book[0], book[1]
		detail = library.get_book_detail(book[0])
		for d in detail:
			print d[0]
			print d[1], d[2]
			for dd in d[3]:
				print dd[0], dd[1], dd[2]
			print '\n\n'