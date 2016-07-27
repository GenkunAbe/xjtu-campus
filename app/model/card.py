# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import cookielib
import cStringIO

from PIL import Image, ImageEnhance
from pytesseract import *
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


class Card:

	def __init__(self, usr, psw):

		self.urls = {
			'basic_info' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/BasicInfo',
			# URL of main page
			'card' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/Transfer',
			# URL to get check code
			'code' : 'http://card.xjtu.edu.cn/Account/GetCheckCodeImg?rad=',
			# URL to get keyboard layout
			'keyboard' : 'http://card.xjtu.edu.cn/Account/GetNumKeyPadImg',
			# URL to post requeset
			'pay' : 'http://card.xjtu.edu.cn/CardManage/CardInfo/TransferAccount',
		}

		self.cas = Cas(usr, psw)


	# Get grades page
	def get_main_page(self):
		# Get card page
		result = self.cas.opener.open(self.urls['card'])
		return result.read()


	def pay(self, psw, check_code, amt):
		self.postdata = urllib.urlencode({
			'password' : psw,
			'checkCode' : check_code,
			'amt' : amt,
			'fcard' : 'bcard',
			'tocard' : 'card',
			'bankno' : '',
			'bankpwd' : ''
		})
		request = urllib2.Request(
			url = self.urls['pay'],
			data = self.postdata,
			headers = ua
		)
		result = self.opener.open(request)
		return result.read()


	def get_code_pic(self, html):
		pattern = re.compile(r'rad=(\d+)"')
		rad = re.findall(pattern, html)[0]
		result = self.opener.open(self.urls['code'] + rad)
		with open('1.gif', 'wb') as f:
			f.write(result.read())


	def get_encoded_psw(self, psw):
		result = self.opener.open(self.urls['keyboard'])
		stream = cStringIO.StringIO(result.read())
		img = Image.open(stream)
		img = ImageEnhance.Brightness(img).enhance(1.1)
		new_img = Image.new('L', (130, 25))
		for j in range(10):
			tmp = img.crop((6+j*30, 3, 19+j*30,28))
			new_img.paste(tmp, (j*13,0))
		ss = image_to_string(new_img, lang = 'num')
		ans = ''
		for i in psw:
			for j in range(len(ss)):
				if i == ss[j]:
					ans += str(j)
		return ans[::-1]


	def get_card_info(self):
		result = self.cas.opener.open(self.urls['basic_info'])
		html = result.read()

		pattern = re.compile(r'<em>(.+?)</em>', re.S)
		data = re.findall(pattern, html)
		info = {}
		info['balance'] = data[4]
		info['temp'] = data[5]
		info['loss'] = data[6]
		info['freeze'] = data[7]

		return info


if __name__ == '__main__':
	card = Card()
	html = card.get_main_page()
	card.get_code_pic(html)
	raw_psw = str(input('Enter your password: '))
	code = str(input('Enter check Code: '))
	amt = input('Enter amount of money: ')
	psw = card.get_encoded_psw(raw_psw)
	result = card.pay(psw, code, '%.2f' % float(amt))
	print result

