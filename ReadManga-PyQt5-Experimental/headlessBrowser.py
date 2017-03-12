import sys  
import re
import urllib
import time
import os
import os.path
import sys
import calendar
import weakref
import threading
from bs4 import BeautifulSoup
from datetime import datetime
import pycurl
import subprocess
from io import StringIO,BytesIO
from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtNetwork import QNetworkAccessManager

class BrowseUrl(QWebEngineView):
	
	def __init__(self,url,quality,c):
		super(BrowseUrl, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.quality = quality
		self.media_val = ''
		self.cnt = 0
		self.cookie_file = c
		self.Browse(self.url)
		
	def Browse(self,url):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		html = ''
		home1 = os.path.expanduser("~")
		
		BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))
		
		enginePath = os.path.join(BASEDIR,'headlessEngine.py')
		
		tmp_dir,new_c = os.path.split(self.cookie_file)
		
		
		content = 'checking_browser'
		#web = BrowseUrl(url,quality)
		if 'checking_browser' in content:
			if os.name == 'posix':
				p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,self.cookie_file])
			else:
				p = subprocess.Popen(['python','-B',enginePath,url,self.quality,self.cookie_file],shell=True)
			
			cnt = 0
			
			lnk_file = os.path.join(tmp_dir,'lnk.txt')
			if os.path.exists(lnk_file):
				os.remove(lnk_file)
			while(not os.path.exists(self.cookie_file) and cnt < 20):
				print(cnt)
				print('wait Clouflare ')
				time.sleep(1)
				cnt = cnt+1
					
			p.kill()
		else:
			f = open(self.cookie_file,'w')
			f.close()
		


