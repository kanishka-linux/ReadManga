"""
This file is part of ReadManga.

ReadManga is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ReadManga is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ReadManga.  If not, see <http://www.gnu.org/licenses/>.



"""

from PyQt5 import QtCore, QtGui,QtWidgets
import sys
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup 
import os.path
from os.path import expanduser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import shutil
from tempfile import mkstemp
from shutil import move
from os import remove, close
import fileinput
import codecs
import base64
from headlessBrowser import BrowseUrl
import hashlib
from binascii import unhexlify, b2a_base64, hexlify
from Crypto.Cipher import AES
import base64
import urllib.parse

def cloudfare(url,q,c):
	web = BrowseUrl(url,q,c)
def getContentUnicode(content):
	if isinstance(content,bytes):
		print("I'm byte")
		try:
			content = str((content).decode('utf-8'))
		except:
			content = str(content)
	else:
		print(type(content))
		content = str(content)
		print("I'm unicode")
	return content

def cloudfareOld(url):
			home1 = expanduser("~")
			pluginDir = "/usr/share/ReadManga/ka.js"
			if os.path.exists(pluginDir):
				plugin_path = pluginDir
			else:
				plugin_path = home1+"/.config/ReadMangaKA/src/ka.js"
			temp = progressBar(["phantomjs", plugin_path,"http://kissmanga.com"])
			temp = getContentUnicode(temp)
			print (temp)
			p = re.findall('{[^}]*}',temp)
			for i in p:
				if "_cfduid" in i:
					cfd = i
				elif "cf_clearance" in i:
					cfc = i

			n = re.findall('value": "[^"]*|expiry": [^,]*',cfc)
			e = re.findall('value": "[^"]*|expiry": [^,]*',cfd)
			j = 0
			for i in n:
				n[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			j = 0
			for i in e:
				e[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			cookiefile = ".kissmanga.com	TRUE	/	FALSE	"+str(e[0])+"	__cfduid	" + str(e[1]) + "\n" + ".kissmanga.com	TRUE	/	FALSE	"+str(n[0])+"	cf_clearance	" + str(n[1] + "\n" + "kissmanga.com	FALSE	/	FALSE	0	usingFlashV1	true")
			f = open('/tmp/ReadManga/kcookieM.txt', 'w')
			f.write(cookiefile)
			f.close()


def ccurl(url):
	global hdr
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	print(url)
	c = pycurl.Curl()
	
	
	curl_opt = ''
	picn_op = ''
	rfr = ''
	nUrl = url
	cookie_file = ''
	if '#' in url:
		curl_opt = nUrl.split('#')[1]
		url = nUrl.split('#')[0]
		if curl_opt == '-o':
			picn_op = nUrl.split('#')[2]
		elif curl_opt == '-Ie':
			rfr = nUrl.split('#')[2]
		elif curl_opt == '-Icb' or curl_opt == '-bc' or curl_opt == '-b' or curl_opt == '-Ib':
			cookie_file = nUrl.split('#')[2]
	url = str(url)
	print(url,'----------url------')
	c.setopt(c.URL, url.encode('utf-8'))
	storage = BytesIO()
	if curl_opt == '-o':
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, hdr)
		f = open(picn_op,'wb')
		c.setopt(c.WRITEDATA, f)
		c.perform()
		c.close()
		f.close()
	else:
		if curl_opt == '-I':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-Ie':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(pycurl.REFERER, rfr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-IA':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-Icb':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
			if os.path.exists(cookie_file):
				os.remove(cookie_file)
			c.setopt(c.COOKIEJAR,cookie_file)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-Ib':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-bc':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEJAR,cookie_file)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-b':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-L':
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		else:
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		try:
			c.perform()
			c.close()
			content = storage.getvalue()
			content = getContentUnicode(content)
		except Exception as e:
			print(e)
			content = ''
		return content


def progressBar(cmd):
	MainWindow = QtWidgets.QWidget()
	progress = QtWidgets.QProgressDialog("Please Wait!", "Cancel", 0, 100, MainWindow)
	progress.setWindowModality(QtCore.Qt.WindowModal)
	progress.setAutoReset(True)
	progress.setAutoClose(True)
	progress.setMinimum(0)
	progress.setMaximum(100)
	progress.resize(500,100)
	progress.setWindowTitle("Loading, Please Wait! (Cloudflare Protection)")
	progress.show()
	progress.setValue(0)
	#content = cmd
	#print content
	#content = ccurl(cmd,"")
	content = subprocess.check_output(cmd)
	
	progress.setValue(100)
	progress.hide()
	#print content
	return content


def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def replace_all(text, di):
	for (i, j,) in di.iteritems():
		text = text.replace(i, j)

	return text

def get_code_val():
	_0x331e=["\x6C\x69\x62","\x57\x6F\x72\x64\x41\x72\x72\x61\x79","\x48\x61\x73\x68\x65\x72","\x61\x6C\x67\x6F","\x73\x71\x72\x74","\x70\x6F\x77","\x53\x48\x41\x32\x35\x36","\x5F\x68\x61\x73\x68","\x73\x6C\x69\x63\x65","\x69\x6E\x69\x74","\x77\x6F\x72\x64\x73","\x5F\x64\x61\x74\x61","\x5F\x6E\x44\x61\x74\x61\x42\x79\x74\x65\x73","\x73\x69\x67\x42\x79\x74\x65\x73","\x66\x6C\x6F\x6F\x72","\x6C\x65\x6E\x67\x74\x68","\x63\x61\x6C\x6C","\x63\x6C\x6F\x6E\x65","\x65\x78\x74\x65\x6E\x64","\x48\x6D\x61\x63\x53\x48\x41\x32\x35\x36","\x61\x35\x65\x38\x65\x32\x65\x39\x63\x32\x37\x32\x31\x62\x65\x30\x61\x38\x34\x61\x64\x36\x36\x30\x63\x34\x37\x32\x63\x31\x66\x33","\x6D\x73\x68\x73\x64\x66\x38\x33\x32\x6E\x73\x64\x62\x61\x73\x68\x32\x30\x61\x73\x64\x6D","\x70\x61\x72\x73\x65","\x48\x65\x78","\x65\x6E\x63","\x42\x61\x73\x65\x36\x34","\x63\x72\x65\x61\x74\x65","\x43\x69\x70\x68\x65\x72\x50\x61\x72\x61\x6D\x73","\x43\x42\x43","\x6D\x6F\x64\x65","\x50\x6B\x63\x73\x37","\x70\x61\x64","\x64\x65\x63\x72\x79\x70\x74","\x41\x45\x53"]
	
	return _0x331e[21]

def decrypt_url(url,req_key):
	
	_0x331e=["\x6C\x69\x62","\x57\x6F\x72\x64\x41\x72\x72\x61\x79","\x48\x61\x73\x68\x65\x72","\x61\x6C\x67\x6F","\x73\x71\x72\x74","\x70\x6F\x77","\x53\x48\x41\x32\x35\x36","\x5F\x68\x61\x73\x68","\x73\x6C\x69\x63\x65","\x69\x6E\x69\x74","\x77\x6F\x72\x64\x73","\x5F\x64\x61\x74\x61","\x5F\x6E\x44\x61\x74\x61\x42\x79\x74\x65\x73","\x73\x69\x67\x42\x79\x74\x65\x73","\x66\x6C\x6F\x6F\x72","\x6C\x65\x6E\x67\x74\x68","\x63\x61\x6C\x6C","\x63\x6C\x6F\x6E\x65","\x65\x78\x74\x65\x6E\x64","\x48\x6D\x61\x63\x53\x48\x41\x32\x35\x36","\x61\x35\x65\x38\x65\x32\x65\x39\x63\x32\x37\x32\x31\x62\x65\x30\x61\x38\x34\x61\x64\x36\x36\x30\x63\x34\x37\x32\x63\x31\x66\x33","\x6D\x73\x68\x73\x64\x66\x38\x33\x32\x6E\x73\x64\x62\x61\x73\x68\x32\x30\x61\x73\x64\x6D","\x70\x61\x72\x73\x65","\x48\x65\x78","\x65\x6E\x63","\x42\x61\x73\x65\x36\x34","\x63\x72\x65\x61\x74\x65","\x43\x69\x70\x68\x65\x72\x50\x61\x72\x61\x6D\x73","\x43\x42\x43","\x6D\x6F\x64\x65","\x50\x6B\x63\x73\x37","\x70\x61\x64","\x64\x65\x63\x72\x79\x70\x74","\x41\x45\x53"]
	
	if req_key:
		if len(req_key) >= 2:
			chko1 = req_key[0]
			chko2 = req_key[1]
		else:
			chko1 = req_key[0]
			chko2 = req_key[0]
	else:
		chko1 = _0x331e[21]
		chko2 = _0x331e[21]
		
	key1 = hashlib.sha256(chko1.encode('utf-8')).digest()
	key2 = hashlib.sha256(chko2.encode('utf-8')).digest()

	boxzq = _0x331e[20]
	chko = _0x331e[21]
	key = hashlib.sha256(chko.encode('utf-8')).digest()
	
	#print(boxzq,len(boxzq))

	m = [_0x331e[24],_0x331e[23],_0x331e[22]]
	IV = unhexlify(bytes(boxzq,'utf-8'))
	print(IV,len(IV))
	cipher = AES.new(key,AES.MODE_CBC,IV)
	cipher1 = AES.new(key1,AES.MODE_CBC,IV)
	cipher2 = AES.new(key2,AES.MODE_CBC,IV)
	#print(cipher1,cipher2)
	cy = url
	x = base64.b64decode(bytes(cy,'utf-8'))
	#print(x,len(x))
	try:
		c = cipher1.decrypt(x)
		y = str(c,'utf-8')
	except Exception as e:
		print(e)
		try:
			c = cipher2.decrypt(x)
			y = str(c,'utf-8')
		except Exception as e:
			print(e)
			c = cipher.decrypt(x)
			y = str(c,'utf-8')
	return y
		
class Manga_Read():
	def __init__(self,site):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		if site == "KissManga":
			if not os.path.isfile('/tmp/ReadManga/kcookieM.txt'):
				cloudfare("http://kissmanga.com",'','/tmp/ReadManga/kcookieM.txt')
		else:
			pass
			
	def ccurlN(self,content,url):
		if 'checking_browser' in content:
			if os.path.exists('/tmp/ReadManga/kcookieM.txt'):
				os.remove('/tmp/ReadManga/kcookieM.txt')
				if '#' in url:
					url1 = url.split('#')[0]
					cloudfare(url1,'','/tmp/ReadManga/kcookieM.txt')
			content = ccurl(url)
		return content
		
	def search(self,site,name):
			if site == "KissManga":
				if name != '':
					url = 'http://kissmanga.com/Search/Manga/?keyword=' + name
					
					content = ccurl(url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
					content = self.ccurlN(content,url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
					print (content)
					
					m = re.findall('/Manga/[^"]*', content)
					#print m
					m = list(set(m))
					m.sort()
					j = 0
					for i in m:
						i = re.sub('/Manga/', '', i)
						m[j] = i
						j = j + 1

					return m
			elif site == "GoodManga":
				if name:
					url = "http://www.goodmanga.net/manga-search?key=" + name
					content = ccurl(url)
					nxt = re.findall('http://www.goodmanga.net/[0-9]*/[^"]*',content)
					nxt= list(set(nxt))
					nxt.sort()
					m = []
					for i in nxt:
						j = i.split("/")[-1]
						k = i.split("/")[-2]
						l = k + "-" + j
						m.append(l)
					return m
			elif site == "MangaBB":
				if name:
					url = "http://www.mangabb.co/manga-search?key=" + name
					content = ccurl(url)
					nxt = re.findall('http://www.mangabb.co/manga/[^"]*',content)
					nxt= list(set(nxt))
					nxt.sort()
					m = []
					for i in nxt:
						j = i.split("/")[-1]
						k = i.split("/")[-2]
						l = k + "-" + j
						m.append(j)
					return m
			elif site == "MangaHere":
				if name:
					url = "http://www.mangahere.co/search.php?name=" + name
					content = ccurl(url)
					nxt = re.findall('http://www.mangahere.co/manga/[^/]*/',content)
					nxt= list(set(nxt))
					nxt.sort()
					m = []
					for i in nxt:
						j = i.split("/")[-2]
						m.append(j)
					return m
			elif site == "MangaReader":
				if name:
					url = "http://www.mangareader.net/search/?w=" + name
					content = ccurl(url)
					soup = BeautifulSoup(content)
					link = soup.findAll('h3')
					m = []
					for i in link:
						j = i.find('a')
						if j and 'href' in str(j):
							k = j['href']
							m.append(k.split('/')[-1])
					
					return m
	def getInfo(self,site,name):
		if site == "KissManga":
			url = 'http://kissmanga.com/Manga/' + name
			print (url)
			content = ccurl(url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
			content = self.ccurlN(content,url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
			f = open('/tmp/ReadManga/1.txt','w')
			f.write(content)
			f.close()
			epl = re.findall('/Manga/' + name + '[^"]*?id[^"]*', content)
			#if not epl:
			#	epl = re.findall('[^"]*?id=[^"]*', content)
			try:
				img = re.findall('http://kissmanga.com/Uploads/Etc/[^"]*.jpg', content)
				if not img:
					img = re.findall('http://cdn.myanimelist.net/[^"]*.jpg', content)	
				print (img)
				#jpgn = img[0].split('/')[-1]
				#print 'Pic Name=' + jpgn
				picn = '/tmp/ReadManga/' + name + '.jpg'
				print (picn)
				#if img:
				#	print (img[0])
				#if not os.path.isfile(picn):
				#	subprocess.call(['curl','-L','-b','/tmp/ReadManga/kcookieM.txt','-A',self.hdr,'-o',picn,img[0]])
			except:
				picn = '/tmp/ReadManga/' + name + '.jpg'
			j = 0
			for i in epl:
				i = re.sub('/Manga/' + name + '/', '', i)
				epl[j] = i
				j = j + 1

			try:
				soup = BeautifulSoup(content)
				link = soup.findAll('tbody')
				summary = ''
				for i in link:
					summary = i.text

				if not summary:
					link = soup.findAll('p')
					j = 0
					for i in link:
						k = str(i)
						if 'Summary' in k and 'class="info"' in k:
							break
						j = j + 1

					sid = j + 1
					if soup.findAll('p')[sid]:
						sumry = soup.findAll('p')[sid].text
						replc = {'&nbsp;': '','\n': '','<p>': '','<br/>': '','</p>': '','<br />': '','style="text-align: justify;"': '','<span >': ''}
						summary = replace_all(sumry, replc)
					else:
						summary = 'No Summary Available'
			except:
				summary = 'Not Available'
			print (summary)
			print (picn)
			#epl=naturallysorted(epl)  
			epl.reverse()
			epl.append(picn)
			epl.append(summary)
			return epl
		elif site == "GoodManga":
			m = []
			nam = name.split('-')
			if len(nam) == 2:
				nam2 = nam[1]
			elif len(nam) > 2:
				length = len(nam) - 1
				i = 2
				nam2 = nam[1]
				while(i<=length):
					nam2 = nam2+'-'+nam[i]
					i = i+1
			url = 'http://www.goodmanga.net/' + nam[0]+'/'+nam2
			print (url)
			content = ccurl(url)
			tmp = re.findall('http://www.goodmanga.net/[^"]*/chapter/[^"]*',content)
			print (tmp)
			url = tmp[0]
			print (url)
			content = ccurl(url)
			soup = BeautifulSoup(content)
			link = soup.find('div',{'id':'asset_1'})
			print (link)
			link1 = link.findAll('option')
			for i in link1:
				j = i['value']
				k = j.split('/')[-1]
				m.append(k)
			m.append('No Picture')
			m.append('No Summary')
			return m
		elif site == "MangaBB":
			m = []
			
			url = 'http://www.mangabb.co/manga/' +name
			print (url)
			content = ccurl(url)
			tmp = re.findall('http://www.mangabb.co/'+name+'/chapter[^"]*',content)
			print (tmp)
			url = tmp[0]
			print (url)
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			link = soup.find('div',{'id':'asset_1'})
			print (link)
			link1 = link.findAll('option')
			for i in link1:
				j = i['value']
				k = j.split('/')[-1]
				m.append(k)
			m.append('No Picture')
			m.append('No Summary')
			return m
		elif site == "MangaReader":
			m = []
			
			url = 'http://www.mangareader.net/' +name
			print (url)
			content = ccurl(url)
			
			soup = BeautifulSoup(content)
			
			link = soup.findAll('table',{'id':'listing'})
			print (link)
			
			
			for i in link:
				j = i.findAll('a')
				for l in j:
					if 'href' in str(l):
						k = l['href']
						m.append(k.split('/')[-1])
			m.append('No Picture')
			m.append('No Summary')
			return m
		elif site == "MangaHere":
			m = []
			url = 'http://www.mangahere.co/manga/' + name+'/'
			print (url)
			content = ccurl(url)
			
			soup = BeautifulSoup(content)
			link = soup.find('div',{'class':'detail_list'})
			#print link
			link1 = link.findAll('a')
			for i in link1:
				if 'href' in str(i):
					j = i['href']
					if 'http' in j:
						k = j.split('/')[-2]
						l = j.split('/')[-3]
						if name == l:
							m.append(k)
						else:
							m.append(l+'-'+k)
			m.reverse()
			m.append('No Picture')
			m.append('No Summary')
			return m
	def getPage(self,site,name,epn):
		if site == "KissManga":
			url = 'http://kissmanga.com/Manga/' + name + '/' + epn
			print (url)
			
			content = ccurl(url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
			content = self.ccurlN(content,url+'#'+'-b'+'#'+'/tmp/ReadManga/kcookieM.txt')
			soup = BeautifulSoup(content)
			#print(soup.prettify())
			
			scripts = soup.findAll('script',{'type':'text/javascript'})
			req_key = []
			chk = ''
			index = 0
			for i in scripts:
				if 'chko = ' in str(i):
					print(i)
					j = i.text.strip()
					k = re.search('var [^;]*',j).group()
					print(k,'------kkkkkkkkkkkkkkk')
					l = re.sub("var |;",'',k).split('=')[1].strip()
					n = eval(l)
					print(n[0])
					chk = re.search('chko = [^;]*',j).group()
					print(chk)
					new_chk = chk.split('=')[1]
					if 'chko' in new_chk and index == 0:
						new_val = get_code_val() + n[0]
					elif 'chko' in new_chk and index == 1:
						new_val = req_key[0] + n[0]
					else:
						new_val = n[0]
					req_key.append(new_val)
					print(req_key)
					index += 1
					
			print(req_key)
			m = re.findall('push[(]wrapKA[(]"[^"]*',content)
			#print m
			arr = []
			for i in m:
				i = re.sub('push[(]wrapKA[(]"','',i)
				#i = re.sub('"','',i)
				#print(i,'----------ii-----------')
				i = decrypt_url(i,req_key)
				j = i.split('.')[-1].lower()
				if j == 'jpg' or j == 'jpeg' or j == 'png':
					pass
				else:
					k = re.findall('http[^"]*.jpg|http[^"]*.jpeg|http[^"]*.JPG|http[^"]*.JPEG|http[^"]*.png|http[^"]*.PNG',i)
					if k:
						i = k[0]
				arr.append(i)
			return arr
		elif site == "GoodManga":
			m = []
			nam = name.split('-')
			if len(nam) == 2:
				nam2 = nam[1]
			elif len(nam) > 2:
				length = len(nam) - 1
				i = 2
				nam2 = nam[1]
				while(i<=length):
					nam2 = nam2+'-'+nam[i]
					i = i+1
			url = 'http://www.goodmanga.net/' +nam2+"/chapter/"+epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			link = soup.find('div',{'id':'asset_2'})
			if link:
				link1 = link.findAll('option')
				num = 1
				url1 = "http://www.goodmanga.net/images/manga/"+nam2+"/"+epn
				for i in link1:
					j = i['value']
					k = j.split('/')[-1]
					m.append(url1+'/'+str(num)+'.jpg')
					num = num+1
			print (m)
			return m
		elif site == "MangaBB":
			m = []
			ep = epn.split('-')
			url = 'http://www.mangabb.co/' +name+"/"+epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			imgLink = soup.find('div',{'id':'manga_viewer'})
			if imgLink:
				imgUrl = (imgLink.find('img'))['src']
				nameImg = imgUrl.split('/')[-3]
				
				link = soup.find('div',{'id':'asset_2'})
				link1 = link.findAll('option')
				num = 1
				nam = name.replace('-','_')
				url1 = "http://www.mangabb.co/images/manga/"+nameImg+"/"+ep[-1]
				for i in link1:
					j = i['value']
					k = j.split('/')[-1]
					m.append(url1+'/'+str(num)+'.jpg')
					num = num+1
			print (m)
			return m
		elif site == "MangaReader":
			m = []
			ep = epn.split('-')
			url = 'http://www.mangareader.net/' +name+"/"+epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			imgLink = soup.find('div',{'id':'imgholder'})
			if imgLink:
				imgUrl = (imgLink.find('img'))['src']
				nameImg = imgUrl.split('/')[-1]
				nameImg = nameImg.replace('.jpg','')
				tName = nameImg.split('-')[-1]
				
				arr = nameImg.split('-')
				arr = arr[:-1]
				p_name = arr[0]
				length = len(arr)
				i = 1
				while(i < length):
					p_name = p_name + '-'+ arr[i]
					i = i+1
					
				urlArr = imgUrl.split('/')
				urlArr = urlArr[:-1]
				p_url = urlArr[0]
				length = len(urlArr)
				i = 1
				while(i < length):
					p_url = p_url + '/' + urlArr[i]
					i = i+1
					
				link = soup.find('div',{'id':'selectpage'})
				link1 = link.findAll('option')
				
				#num = int(tName)
				num = 1
				url1 = p_url+'/'+p_name
				print (url1)
				for i in link1:
					j = i['value']
					k = j.split('/')[-1]
					#m.append(url1+'-'+str(num)+'.jpg')
					m.append("http://www.mangareader.net"+j)
					num = num+1
			print (m)
			return m
		elif site == "MangaHere":
			m = []
			if '-' in epn:
				ep = epn.split('-')
				url = 'http://www.mangahere.co/manga/'+name+'/'+ep[0]+'/'+ep[1]+'/'
			else:
				url = 'http://www.mangahere.co/manga/'+name+'/'+epn+'/'
			print (url)
			content = ccurl(url)
			soup = BeautifulSoup(content)
			link = soup.find('select',{'class':'wid60'})
			if link:
				link1 = link.findAll('option')
			else:
				link1 = []
			
			linkImg = soup.find('section',{'class':'read_img'})
			
			if linkImg:
				urlImg = linkImg.findAll('img')
			else:
				urlImg = []
			try:
				for i in urlImg:
					if 'src=' in str(i):
						url2 = i['src']
						url1 = url2.split('?')[0]
						url1 = url1.replace('.jpg','')
						
				tNum = url1[-1]
				try:
					num = int(tNum)
				except:
					num = 1
				for i in link1:
					j = i['value']
					k = j.split('/')[-1]
					numStr = str(num)
					if len(numStr) == 1:
						urlNew = url1[:-1]
					elif len(numStr) == 2:
						urlNew1 = url1[:-1]
						urlNew = urlNew1[:-1]

					#m.append(urlNew+numStr+'.jpg')
					m.append(j)
					num = num+1
			except:
				pass
			print (m)
			return m
	
	def getPageImg(self,site,name,epn):
		if site == "MangaHere":
			m = []
			url = epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			url1= ""
			
			linkImg = soup.find('section',{'class':'read_img'})
			if linkImg:
				urlImg = linkImg.findAll('img',{'id':'image'})
				for i in urlImg:
					if 'src=' in str(i):
						url1 = i['src']
				print (url1)
			return url1
		elif site == "MangaReader":
			m = []
			url = epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			imgLink = soup.find('div',{'id':'imgholder'})
			if imgLink:
				imgUrl = (imgLink.find('img'))['src']
			else:
				imgUrl = ""
			return imgUrl
			
	
