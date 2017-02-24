# -*- coding: utf-8 -*-

import sys
import os
from cas import Cas
import re
import urllib2
import urllib
import json


ua = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding' : 'gzip, deflate, sdch, br',
	'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
	'Connection' : 'keep-alive',
	'DNT' : '1',
	'Host' : 'ssfw.xjtu.edu.cn',
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}


urls = {
	'home' : 'http://ssfw.xjtu.edu.cn/index.portal',
	'grade' : 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1144_p1156',
	'table' : 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1145_p1542',
	'exam' : 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1147_p1158',
	'mark' : 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1182_p1183',
	'table_list' : 'http://ssfw.xjtu.edu.cn/pnull.portal?.pen=pe801&.pmn=view&action=optionsRetrieve&className=com.wiscom.app.w5ssfw.pkgl.domain.T_PKGL_PKSJSZ&namedQueryId=&displayFormat={xnxqDisplay}&useBaseFilter=true',
	'table_post' : 'http://ssfw.xjtu.edu.cn/index.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjE4MjF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5',
	'teachers_list' : 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1182_p1183',
	'teacher_post' : '',
}


class Ssfw:
	def __init__(self, usr, psw):
		self.usr = usr
		self.psw = psw
		self.cas = Cas(usr, psw)
		if not len(self.cas.link) == 0:
			self.cas.opener.open(self.cas.link[0])
		else:
			# raise Error
			pass


	def get_grades(self, try_again = True):
		grades = []
		result = self.cas.opener.open(urls['grade'])
		html = result.read()

		pattern = re.compile(r'<tr class.+?</tr>', re.S)
		lines = re.findall(pattern, html)

		if len(lines) is 0 and try_again:
			try:
				os.remove('./data/' + self.usr + '/cookie')
				return self.get_grades(try_again = False)
			except:
				return []

		for line in lines:
			pattern = re.compile(r'class="[bjgcss]*">\s*(.*?)\s*</td>', re.S)
			items = re.findall(pattern, line)

			pattern = re.compile(r"'(.*?)'", re.S)
			marks = re.findall(pattern, items[5])
			if not len(marks) == 0:
				items[5] = marks[1:8]
			else:
				tmp = ['' for i in xrange(7)]
				tmp[0] = items[5]
				items[5] = tmp

			grades.append(items)

		return grades

	def auto_assess_teacher(self):
		teachers_list = self.get_teachers_list()
		for line in teachers_list:
			self.assess_teacher(line[7])
			exit()

	def get_teachers_list(self):
		html = self.cas.opener.open(urls['teachers_list']).read()
		pattern = re.compile(r'<tr class.+?<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)&nbsp;\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*<a href="(.*?)">.+?</td></tr>', re.S)
		result = re.findall(pattern, html)
		return result
	
	def assess_teacher(self, url, auto=True, overview=None, rate=None, suggestion=None):
		html = self.cas.opener.open(urls['home'] + url).read()
		pattern = re.compile(r'<td style="vertical-align:middle">(.+?)</tr>', re.S)
		lines = re.findall(pattern, html)
		pattern = re.compile(r'<input.+?name="(.+?)".+?value="(.+?)".+?/>', re.S)
		for line in lines:
			items = re.findall(pattern, line)
			print items

	def get_table(self):
		table = []
		result = self.cas.opener.open(urls['table'])
		html = result.read()

		return self.table_parser(html)


	def get_priv_table(self, term = '20152'):
		postdata = urllib.urlencode({
			'newSearch' : 'true',
			'xnxqdm' : term
		})
		request = urllib2.Request(
			url =  urls['table_post'],
			data = postdata,
			headers = ua
		)
		result = self.cas.opener.open(request)
		html = result.read()

		return self.table_parser(html)


	def table_parser(self, html):
		table = []
		pattern = re.compile(r'</div>&nbsp;(.+?)\s*</td>')
		divs = re.findall(pattern, html)
		for div in divs:
			infos = re.split(r'<br>|&nbsp;|~|-', div)
			if len(infos) > 8 and (len(infos) % 8 == 0):
				for i in xrange(len(infos) / 8):
					table.append(infos[8 * i : 8 * (i + 1)])
			else:
				table.append(infos)

		for i in range(len(table)):
			pattern = re.compile(r'\((.+?)\)', re.S)
			result = re.findall(pattern, table[i][3])
			if len(result) == 1:
				if result[0] == '\xe5\x8d\x95':
					table[i].append('1')
				else:
					table[i].append('2')
			else:
				table[i].append('0')
			
			pattern = re.compile(r'[\d]+')
			table[i][3] = re.findall(pattern, table[i][3])[0]
			table[i][5] = re.findall(pattern, table[i][5])[0]
			table[i][6] = re.findall(pattern, table[i][6])[0]

			table[i][7] = table[i][7][1:-1]			
			
		return table


	def get_table_list(self):
		result = self.cas.opener.open(urls['table_list'])
		return json.load(result)


	def auto_judge(self):
		pass

if __name__ == '__main__':
	usr = sys.argv[1]
	psw = sys.argv[2]
	ssfw = Ssfw(usr, psw)

	ssfw.auto_assess_teacher()
	exit()


	grades = ssfw.get_grades()
	for grade in grades:
	  print '\t'.join([str(i) for i in grade])
	exit()

	table_list = ssfw.get_table_list()

	table = ssfw.get_old_table(table_list['options'][2]['code'])
	for course in table:
		print '\t\t\t'.join(course)