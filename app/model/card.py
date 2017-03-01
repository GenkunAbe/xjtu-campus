# -*- coding: utf-8 -*-

import sys
import re
import urllib
import urllib2
import base64

from cas import Cas


ua = {
	'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding' : 'gzip, deflate, sdch, br',
	'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
	'Connection' : 'keep-alive',
	'DNT' : '1',
	'Host' : 'card.xjtu.edu.cn',
	'Upgrade-Insecure-Requests' : '1',
	'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

urls = {
	# URL of home page
	'home' : 'http://card.xjtu.edu.cn/',
	# URL of vasic information
	'basic_info' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/BasicInfo',
	# URL of main page
	'card' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/Transfer',
	# URL to get captcha
	'code' : 'http://card.xjtu.edu.cn/Account/GetCheckCodeImg?rad=',
	# URL to change captcha
	'change_code' : 'http://card.xjtu.edu.cn/Account/GetCheckCodeImg/Flag=',
	# URL to get keyboard layout
	'keyboard' : 'http://card.xjtu.edu.cn/Account/GetNumKeyPadImg',
	# URL to post requeset
	'pay' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/TransferAccount',
	# URL to Open Auto Pay Page
	'auto_pay_page' : 'http://card.xjtu.edu.cn:8070/SynCard/Manage/Transfer',
	# URL to Do Auto Pay
	'auto_pay' : 'http://card.xjtu.edu.cn:8070/SynCard/Manage/TransferPost',
}


class Card:

	def __init__(self, usr, psw):

		self.usr = usr
		self.psw = psw

		self.cas = Cas(usr, psw)

	def auto_pay(self, amt, psw):
		postdata = urllib.urlencode([
				('FromCard', 'bcard'),
				('ToCard', 'card'),
				('Amount', amt),
				('Password', psw)
			])
		request = urllib2.Request(
			url = urls['auto_pay'],
			data = postdata,
			headers = ua
		)
		# result = self.cas.opener.open('http://card.xjtu.edu.cn:8070/')
		self.cas.opener.open(urls['auto_pay_page'])
		self.cas.opener.open(urls['auto_pay_page'])		
		result = self.cas.opener.open(request)
		return result.read()


	def get_card_info(self):
		result = self.cas.opener.open(urls['home'])		
		result = self.cas.opener.open(urls['basic_info'])
		html = result.read()

		info = {}
		try:
			pattern = re.compile(r'<em>(.+?)</em>', re.S)
			data = re.findall(pattern, html)
			info['balance'] = data[4]
			info['temp'] = data[5]
			info['loss'] = data[6]
			info['freeze'] = data[7]
		except:
			info['balance'] = '-1'
			info['temp'] = '-1'
			info['loss'] = '-1'
			info['freeze'] = '-1'

		return info


if __name__ == '__main__':
	usr = sys.argv[1]
	psw = sys.argv[2]

	card = Card(usr, psw)

	amt = raw_input("AMT: ")
	psw = raw_input("PSW: ")
	psw = base64.b64encode(psw)
	print(psw)
	result = card.auto_pay(amt, psw)
	print(result)
	exit()

	print(card.get_card_info())
	exit()



