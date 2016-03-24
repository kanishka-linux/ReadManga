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
import urllib
import urllib3
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
from PyQt5.QtWebKit import *
import time
import shutil
from tempfile import mkstemp
from shutil import move
from os import remove, close
import fileinput
import codecs
import base64

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

def cloudfare(url):
			home1 = expanduser("~")
			pluginDir = home1+"/.config/ReadMangaKA/src"
			temp = progressBar(["phantomjs", pluginDir+"/ka.js","http://kissmanga.com"])
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
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
	
	c = pycurl.Curl()
	c.setopt(c.USERAGENT, hdr)
	if os.path.isfile('/tmp/ReadManga/kcookieM.txt'):
		c.setopt(c.COOKIEFILE, '/tmp/ReadManga/kcookieM.txt')
	url = str(url)
	c.setopt(c.URL, url)
	#storage = StringIO()
	storage = BytesIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
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



class Manga_Read():
	def __init__(self,site):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		if site == "KissManga":
			if not os.path.isfile('/tmp/ReadManga/kcookieM.txt'):
				cloudfare("url")
		else:
			pass
	def search(self,site,name):
			if site == "KissManga":
				if name != '':
					url = 'http://kissmanga.com/Search/Manga/?keyword=' + name
					
					content = ccurl(url)
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
			content = ccurl(url)
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
				if img:
					#img[0]=img[0].replace('kissanime.com','kissmanga.com')
					print (img[0])
				if not os.path.isfile(picn):
					subprocess.call(['curl','-L','-b','/tmp/ReadManga/kcookieM.txt','-A',self.hdr,'-o',picn,img[0]])
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
			
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			m = re.findall('push[(]"http://[^"]*.jpg|push[(]"http://[^"]*.png|push[(]"https://[^"]*.jpg|push[(]"https://[^"]*.png',content)
			#print m
			arr = []
			for i in m:
				i = re.sub('push[(]"','',i)
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
			
			link1 = link.findAll('option')
			
			linkImg = soup.find('section',{'class':'read_img'})
			
			urlImg = linkImg.findAll('img')
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
			print (m)
			return m
	
	def getPageImg(self,site,name,epn):
		if site == "MangaHere":
			m = []
			url = epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			
			linkImg = soup.find('section',{'class':'read_img'})
			
			urlImg = linkImg.findAll('img')
			for i in urlImg:
				if 'src=' in str(i):
					url2 = i['src']
					url1 = url2.split('?')[0]
			
			print (url1)
			return url1
		elif site == "MangaReader":
			m = []
			url = epn
			content = ccurl(url)
			soup = BeautifulSoup(content)
			imgLink = soup.find('div',{'id':'imgholder'})
			imgUrl = (imgLink.find('img'))['src']
			return imgUrl
			
	
