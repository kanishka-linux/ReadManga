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
import urllib.parse
import pycurl
from io import StringIO,BytesIO    
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from functools import partial
from os.path import expanduser
from Manga_Read import Manga_Read
import weakref
import imghdr
from PIL import Image 
import time
import threading
from PyQt5.QtCore import (QCoreApplication, QObject, Q_CLASSINFO, pyqtSlot,pyqtSignal,
                          pyqtProperty)
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
	c.setopt(c.URL, url)
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
		c.perform()
		c.close()
		content = storage.getvalue()
		content = getContentUnicode(content)
		return content
		
class downloadThread(QtCore.QThread):
    
	def __init__(self,url):
		QtCore.QThread.__init__(self)
	
		self.url = url
		self.interval = 1

	def __del__(self):
		self.wait()                        
	
	def run(self):
		ccurl(self.url)

class downloadFile(QtCore.QThread):
	imgAvailable = pyqtSignal(str,int)
	def __init__(self,pic,label_num):
		QtCore.QThread.__init__(self)
		self.picn = pic
		self.label_num = label_num
		self.interval = 1

	def __del__(self):
		self.wait()                        
	
	def run(self):
		img_err = True
		load_try = 0
		picN = self.picn
		num = self.label_num
		while(img_err and load_try < 1800):
			#print(load_try)
			try:
				im = Image.open(picN)
				im.verify()
				im = Image.open(picN)
				im.load()
				img_err = False
			except:
				img_err = True
				
			time.sleep(1)
			load_try = load_try + 1
		print('inside---downloadfile---')
		if not img_err:
			self.imgAvailable.emit(picN,num)

@pyqtSlot(str,int)
def imgReadyNew(p,n):
	global ui
	print(len(ui.imgArr))
	img1 = QtGui.QPixmap(p, "1")
	p7 = "ui.label_"+str(n)+".setPixmap(img1)"
	exec (p7)

@pyqtSlot(str,str,int)
def downloadUrl_thread_finished(url,pic,num):
	global ui
	if url:
		ui.downloadWget.append(downloadThread(url+'#'+'-o'+'#'+pic))
		indxn = len(ui.downloadWget)-1
		ui.downloadWget[indxn].finished.connect(lambda:ui.download_thread_finished(indxn,pic,num))
		ui.downloadWget[indxn].start()
	else:
		ui.createLabel(pic,num)

class downloadUrl(QtCore.QThread):
	imgUrl = pyqtSignal(str,str,int)
	def __init__(self,site,name,pgn,p,n):
		QtCore.QThread.__init__(self)
		
		self.site = site
		self.name = name
		self.pgn = pgn
		self.pic = p
		self.label = n
	def __del__(self):
		self.wait()                        
	
	def run(self):
		ka = Manga_Read(site)
		imgUrl1 = ka.getPageImg(self.site,self.name,self.pgn) 
		del ka
		self.imgUrl.emit(imgUrl1,self.pic,self.label)

class List3(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List3, self).__init__(parent)

	def keyPressEvent(self, event):
		global home,name,site
		if event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				self.setCurrentRow(0)
			else:
				self.setCurrentRow(nextr)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				self.setCurrentRow(self.count()-1)
			else:
				self.setCurrentRow(prev_r)
		
		
		elif event.key() == QtCore.Qt.Key_Return:
			ui.setname()
		
		elif event.key() == QtCore.Qt.Key_Delete:
			if site != "Source":
				dir_path = home+'/'+site
				
				index = self.currentRow()
				item_r  = self.item(index)
				if item_r:
					item = str(self.currentItem().text())
					
					file_pls = dir_path+'/'+item+'.txt'
					if os.path.exists(file_pls):
						os.remove(file_pls)
						self.takeItem(index)
						del item_r
						

class ExtendedQLabel(QtWidgets.QLabel):

	def __init(self, parent):
		QLabel.__init__(self, parent)
	
	
	def mouseReleaseEvent(self, ev):
		global chapterNo,pageNo,arrPage,name,t_width
		#def mouseDoubleClickEvent(self,ev):
		
		#self.emit(QtCore.SIGNAL('clicked()'))
		#sending_button = self.sender()
		t=str(self.objectName())
		print (t)
		if 'label_text_' in t:
			t1 = re.sub('label_text_','',t)
		else:
			t1 = re.sub('label_','',t)
		num = int(t1)
		print (num)
		print (self.text())
		
		p7 = "ui.label_text_"+str(num)+".text()"
		try:
			epn=eval(p7)
			print (epn)
		except:
			return 0
		
		picn = "/tmp/ReadManga/"+str(epn)
		if ev.button() == QtCore.Qt.LeftButton:
			if os.path.exists(picn):
				img1 = QtGui.QPixmap(picn, "1")
				print (t)
				if 'label_text_' in t:
					p7 = "ui.label_"+str(num)+".setPixmap(img1)"
					exec (p7)
					#p9 = "ui.label_"+str(num)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 16777215))"
					#p10 = "ui.label_"+str(num)+".setMinimumSize(QtCore.QSize("+str(t_width)+", 0))"
					#exec (p9)
					#exec (p10)
				else:
					self.setPixmap(img1)
					#p9 = "ui.label_"+str(num)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 16777215))"
					#p10 = "ui.label_"+str(num)+".setMinimumSize(QtCore.QSize("+str(t_width)+", 0))"
					#exec (p9)
					#exec (p10)
				print ("Exists")
			
		
		
		QtWidgets.QApplication.processEvents()
		
	def keyPressEvent(self, event):	
		global frame_toggle,name,label_no,chapterNo,arrPage,pageNo,label_no,t_width,scale_width
		if event.key() == QtCore.Qt.Key_Delete:
			t=str(self.objectName())
			print (t)
			if 'label_text_' in t:
				t1 = re.sub('label_text_','',t)
			else:
				t1 = re.sub('label_','',t)
			num = int(t1)
			print (num)
			print (self.text())
			p7 = "ui.label_text_"+str(num)+".text()"
			epn=eval(p7)
			print (epn)
			picn = "/tmp/ReadManga/"+str(epn)
			if os.path.exists(picn):
				os.remove(picn)
				print(picn+' Removed')
			

class MyScrollArea(QtWidgets.QScrollArea):
	def __init__(self, parent):
		super(MyScrollArea, self).__init__(parent)
		global frame_toggle
		frame_toggle = 0
	
	def scale_content(self):
		global frame_toggle,name,label_no,chapterNo,arrPage,pageNo,label_no,t_width,scale_width,scale_height,strict_original
		strict_original = False
		for i in range(label_no):
			
			
			
			try:
				p10 = "ui.label_"+str(i)+".setScaledContents(True)"
				exec (p10)
				p11 = "ui.label_text_"+str(i)+".setScaledContents(True)"
				exec (p11)
			except:
				pass
	
	def find_size(self):
		global frame_toggle,name,label_no,chapterNo,arrPage,pageNo,label_no,t_width,scale_width,scale_height
		p7 = "ui.label_text_"+str(label_no-1)+".text()"
		try:
			epn=eval(p7)
			print (epn)
			picn = "/tmp/ReadManga/"+str(epn)
			if os.path.exists(picn):
				im = Image.open(picn)
				sz = im.size
				t_width = str(sz[0])
				scale_width = sz[0]
				scale_height = sz[1]
				print('---original dimensions----',sz)
		except:
			t_width = str(900)
			scale_width = t_width
			scale_height = 0
	
	def keyPressEvent(self, event):
		global frame_toggle,name,label_no,chapterNo,arrPage,pageNo,label_no,t_width,view_mode,scale_width,scale_height,strict_original,arr_pg_cnt,view_mode,total_ht
		
		
		if event.modifiers() == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_W:
			if strict_original:
				self.scale_content()
			t_width = str(self.width())
			wd = int(t_width)
			scale_width = wd
			sz = str(scale_width)+','+str(scale_height)
			for i in range(label_no):
				try:
					p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(wd)+", 16777215))"
					p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
					exec (p9)
					exec (p10)
					p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(wd)+", 16777215))"
					exec (p11)
				except:
					pass
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
		elif event.key() == QtCore.Qt.Key_W:
			if strict_original:
				self.scale_content()
			t_width = str(self.width())
			wd = int(t_width)
			self.find_size()
			
			sw = int(scale_width)
			sh = int(scale_height)
			print(scale_width,scale_height)
			if wd > sw:
				d = (wd - sw)/(sw)
				scale_width = wd
				scale_height = scale_height + (scale_height*d)
				print(scale_width,scale_height)
			elif wd < sw:
				d = (sw-wd)/(wd)
				scale_width = wd
				scale_height = scale_height - (scale_height*d)
			sz = str(scale_width)+','+str(scale_height)
			print (t_width)
			for i in range(label_no):
				try:
					p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(wd)+", 16777215))"
					p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
					exec (p9)
					exec (p10)
					p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(wd)+", 16777215))"
					exec (p11)
					QtWidgets.QApplication.processEvents()
				except:
					pass
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
			#QtWidgets.QApplication.processEvents()
		elif event.key() == QtCore.Qt.Key_H:
			if strict_original:
				self.scale_content()
			ht = int(self.height())
			self.find_size()
			
			sw = int(scale_width)
			sh = int(scale_height)
			print(scale_width,scale_height)
			if ht < sh:
				d = (sh-ht)/(sh)
				scale_height = ht
				scale_width = scale_width - (scale_width*d)
				print(scale_width,scale_height)
			elif ht > sh:
				d = (ht-sh)/(sh)
				scale_height = ht
				scale_width = scale_width + (scale_width*d)
			sz = str(scale_width)+','+str(scale_height)
			print ('--height--',ht)
			print ('--new_size--',sz)
			for i in range(label_no):
				try:
					p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
					exec (p9)
					exec (p10)
					p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					exec (p11)
				except:
					pass
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
		elif event.key() == QtCore.Qt.Key_O:
			if strict_original:
				self.scale_content()
			self.find_size()
			sz = str(scale_width)+','+str(scale_height)
			print (t_width)
			for i in range(label_no):
				try:
					p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
					exec (p9)
					exec (p10)
					p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					exec (p11)
				except:
					pass
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
		elif event.key() == QtCore.Qt.Key_Equal:
			if strict_original:
				self.scale_content()
			if not scale_height:
				self.find_size()
			scale_width = scale_width + (scale_width * 0.01)
			scale_height = scale_height + (scale_height * 0.01)
			t_width = scale_width
			sz = str(scale_width)+','+str(scale_height)
			for i in range(label_no):
				try:
					p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
					exec (p9)
					exec (p10)
					p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
					exec (p11)
				except:
					pass
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
		elif event.key() == QtCore.Qt.Key_Minus:
			if strict_original:
				self.scale_content()
			if not scale_height:
				self.find_size()
			scale_width = scale_width - (scale_width * 0.01)
			scale_height = scale_height - (scale_height * 0.01)
			t_width = scale_width
			sz = str(scale_width)+','+str(scale_height)
			if self.height() <= scale_height:
				for i in range(label_no):
					try:
						p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
						p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
						exec (p9)
						exec (p10)
						p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
						exec (p11)
					except:
						pass
				#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
				#ui.scrollArea.verticalScrollBar().setValue(total_height)
		elif event.key() == QtCore.Qt.Key_A:
			
			if not strict_original:
				#total_ht = 0
				strict_original = True
				for i in range(label_no):
					try:
						p10 = "ui.label_"+str(i)+".setScaledContents(False)"
						exec (p10)
						p11 = "ui.label_text_"+str(i)+".setScaledContents(False)"
						exec (p11)
					except:
						pass
					
					p7 = "ui.label_text_"+str(i)+".text()"
					try:
						epn=eval(p7)
						print (epn)
						picn = "/tmp/ReadManga/"+str(epn)
						if os.path.exists(picn):
							im = Image.open(picn)
							sz = im.size
							wd = sz[0]
							ht = sz[1]
							print('---original dimensions----',sz)
					except:
						wd = 900
						ht = 0
					sz = str(int(wd))+','+str(int(ht))
					try:
						p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+sz+"))"
						p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+sz+"))"
						exec (p9)
						exec (p10)
						p11 = "ui.label_text_"+str(i)+".setMaximumSize(QtCore.QSize("+sz+"))"
						exec (p11)
					except:
						pass
			
					#total_ht = total_ht + ht
			print ('---------strict_original--------',strict_original)
			#total_height = ((label_no-1)*scale_height)+((label_no-1)*10)
			#ui.scrollArea.verticalScrollBar().setValue(total_height)
			total_ht = -1
			scale_width = 0
			scale_height = 0
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Left:
			r = ui.list2.currentRow()
			if len(ui.downloadWget) == 0:
				if r > 0:
					r = r-1
					ui.list2.setCurrentRow(r)
					ui.setchapter2()
				
				else:
					r = 0
					ui.list2.setCurrentRow(r)
					ui.setchapter2()
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
			#ui.hello(pageNo)
			#view_mode = 1
			r = ui.list2.currentRow()
			if len(ui.downloadWget) == 0:
				if r < 0:
					r = 0
				if r < ui.list2.count()-1:
					print(r,'---page--number---')
					r = r+1
					ui.list2.setCurrentRow(r)
					ui.setchapter2()
		elif event.key() == QtCore.Qt.Key_F:
			ui.fullscreen()
		elif event.key() == QtCore.Qt.Key_1:
			view_mode = 1
			length = len(arr_pg_cnt)
			length1 = len(arr_pg_cnt)
			ht = 0
			while length >= 6:
				pg_del = arr_pg_cnt[0]
				del arr_pg_cnt[0]
				
				try:
					t = "ui.label_"+str(pg_del)+".height()"

					ht = eval(t)
					total_ht = total_ht - ht
					
					t = "ui.label_"+str(pg_del)+".deleteLater()"

					exec (t)
					t = "ui.label_text_"+str(pg_del)+".deleteLater()"

					exec (t)
				except:
					pass
				length = length - 1
			
			print(len(arr_pg_cnt),'--arr_pg_cnt----')
			val = ui.scrollArea.verticalScrollBar().maximum() - ht - 80
			ui.scrollArea.verticalScrollBar().setValue(val)
		elif event.key() == QtCore.Qt.Key_2:
			view_mode = 2
		elif event.key() == QtCore.Qt.Key_D:
			ui.onlyDownload()
		elif event.key() == QtCore.Qt.Key_C:
			ui.cancelDownload()
		elif event.key() == QtCore.Qt.Key_I:
			if ui.arrow_timer.isActive():
				ui.arrow_timer.stop()
			ui.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			ui.arrow_timer.start(5000)
		elif event.key() == QtCore.Qt.Key_R:
			#ui.fullscreen()
			print (chapterNo)
			jpgn = (arrPage[pageNo].split('/')[-1])
			pic = "/tmp/ReadManga/" + name + '-'+ chapterNo + "-page-" + jpgn
			print (pic)
			#ui.label.clear()
			img1 = QtGui.QPixmap(pic, "1")
			p7 = "ui.label_"+str(label_no)+".setPixmap(img1)"
			exec (p7)
			#ui.label.setPixmap(img1)
			QtWidgets.QApplication.processEvents()
		elif event.key() == QtCore.Qt.Key_P:
			frame_toggle = 1 -frame_toggle
			if frame_toggle == 1:
				ui.frame.show()
				ui.dockWidget.show()
			else:
				ui.frame.hide()
				ui.dockWidget.hide()
		super(MyScrollArea, self).keyPressEvent(event)   



try:
	fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(800, 600)
		icon = QtGui.QIcon.fromTheme(_fromUtf8(""))
		MainWindow.setWindowIcon(icon)
		#self.centralwidget = QtGui.QWidget(MainWindow)
		#self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		#self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
		self.verticalLayout = QtWidgets.QGridLayout(MainWindow)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setContentsMargins(0,0,0,0)
		#self.scrollArea = QtGui.QScrollArea(self.centralwidget)
		#self.scrollArea = MyScrollArea(self.centralwidget)
		self.scrollArea = MyScrollArea(MainWindow)
		self.scrollArea.setMouseTracking(True)
		self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setMouseTracking(True)
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 604, 489))
		self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
		self.horizontalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.horizontalLayout.setContentsMargins(0,0,0,0)
		#self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
		#self.label.setText(_fromUtf8(""))
		#self.label.setObjectName(_fromUtf8("label"))
		#self.label.setMaximumSize(QtCore.QSize(800, 16777215))
		#self.label.setScaledContents(True)
		#self.horizontalLayout.addWidget(self.label)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.verticalLayout.addWidget(self.scrollArea,0,2,1,1)
		self.horizontalLayout.setAlignment(QtCore.Qt.AlignCenter)
		self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)
		#self.frame = QtGui.QFrame(self.centralwidget)
		self.frame = QtWidgets.QFrame(MainWindow)
		self.frame.setMinimumSize(QtCore.QSize(0, 41))
		self.frame.setMaximumSize(QtCore.QSize(16777215, 27))
		self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.gridLayout = QtWidgets.QGridLayout(self.frame)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.line3 = QtWidgets.QLineEdit(self.frame)
		self.line3.setMinimumSize(QtCore.QSize(0, 0))
		self.line3.setMaximumSize(QtCore.QSize(160, 16777215))
		self.line3.setObjectName(_fromUtf8("line3"))
		self.nextP = QtWidgets.QPushButton(self.frame)
		self.nextP.setObjectName(_fromUtf8("next"))
		self.line2 = QtWidgets.QLineEdit(self.frame)
		self.line2.setMaximumSize(QtCore.QSize(40, 16777215))
		self.line2.setObjectName(_fromUtf8("line2"))
		self.prev = QtWidgets.QPushButton(self.frame)
		self.prev.setObjectName(_fromUtf8("prev"))
		self.fs = QtWidgets.QPushButton(self.frame)
		self.fs.setObjectName(_fromUtf8("fs"))
		self.label2 = QtWidgets.QLabel(self.frame)
		self.label2.setMaximumSize(QtCore.QSize(93, 16777215))
		self.label2.setObjectName(_fromUtf8("label2"))
		self.label3 = QtWidgets.QLabel(self.frame)
		self.label3.setText(_fromUtf8(""))
		self.label3.setObjectName(_fromUtf8("label3"))
		
		self.verticalLayout.addWidget(self.frame,1,2,1,1)
		#MainWindow.setCentralWidget(self.centralwidget)
		
		self.dockWidget = QtWidgets.QDockWidget(MainWindow)
		self.verticalLayout.addWidget(self.dockWidget,0,0,1,1)
		self.dockWidget.setMaximumSize(QtCore.QSize(300, 524287))
		#self.dockWidget.setMiniximumSize(QtCore.QSize(300, 524287))
		self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
		self.dockWidgetContents = QtWidgets.QWidget(MainWindow)
		self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName(_fromUtf8("tab"))
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		
		self.selectSite = QtWidgets.QComboBox(self.tab)
		self.selectSite.setObjectName(_fromUtf8("selectSite"))
		self.verticalLayout_2.addWidget(self.selectSite)
		
		self.select = QtWidgets.QComboBox(self.tab)
		self.select.setObjectName(_fromUtf8("select"))
		self.verticalLayout_2.addWidget(self.select)
		
		self.line1 = QtWidgets.QLineEdit(self.tab)
		self.line1.setObjectName(_fromUtf8("line1"))
		self.verticalLayout_2.addWidget(self.line1)
		self.list3 = List3(self.tab)
		self.list3.setAutoFillBackground(False)
		self.list3.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.list3.setAlternatingRowColors(True)
		self.list3.setWordWrap(False)
		self.list3.setObjectName(_fromUtf8("list3"))
		self.verticalLayout_2.addWidget(self.list3)
		self.tabWidget.addTab(self.tab, _fromUtf8(""))
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.list1 = QtWidgets.QListWidget(self.tab_2)
		self.list1.setObjectName(_fromUtf8("list1"))
		self.horizontalLayout_3.addWidget(self.list1)
		self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
		self.tab_3 = QtWidgets.QWidget()
		self.tab_3.setObjectName(_fromUtf8("tab_3"))
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_3)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.list2 = QtWidgets.QListWidget(self.tab_3)
		self.list2.setObjectName(_fromUtf8("list2"))
		self.horizontalLayout_4.addWidget(self.list2)
		self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
		self.horizontalLayout_2.addWidget(self.tabWidget)
		self.dockWidget.setWidget(self.dockWidgetContents)
		#self.dockWidget.hide()
		#MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
		#self.frame.hide()
		
		self.progress = QtWidgets.QProgressBar(MainWindow)
		#self.progress = QtGui.QProgressBar()
		self.progress.setObjectName(_fromUtf8("progress"))
		#self.gridLayout.addWidget(self.progress, 0, 6, 1, 1)
		self.progress.setMinimum(0)
		self.progress.setMaximum(100)
		self.progress.setMaximumSize(QtCore.QSize(400,16777215))
		self.progress.setTextVisible(True)
		self.progress.hide()
		self.progress.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignCenter)
		
		self.gridLayout.addWidget(self.prev, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
		self.gridLayout.addWidget(self.label3, 0, 1, 1, 1)
		self.gridLayout.addWidget(self.line3, 0, 2, 1, 1)
		self.gridLayout.addWidget(self.label2, 0, 3, 1, 1)
		self.gridLayout.addWidget(self.line2, 0, 4, 1, 1)
		self.gridLayout.addWidget(self.nextP, 0, 5, 1, 1, QtCore.Qt.AlignRight)
		self.gridLayout.addWidget(self.fs, 0, 6, 1, 1, QtCore.Qt.AlignRight)
		self.gridLayout.addWidget(self.progress,0,7,1,1)
		self.horizontalLayout.setAlignment(QtCore.Qt.AlignCenter)
		#self.nxtp = QtGui.QAction(self)
		#QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self.frame, self.hello_next)
		#QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), self.frame, self.previous)
		#QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.frame, self.setpage)
		QtWidgets.QShortcut(QtGui.QKeySequence("F"), self.frame, self.fullscreen)
		
		
		self.select.addItem(_fromUtf8(""))
		self.select.addItem(_fromUtf8(""))
		#self.select.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.selectSite.addItem(_fromUtf8(""))
		self.retranslateUi(MainWindow)
		"""
		QtCore.QObject.connect(self.nextP, QtCore.SIGNAL(_fromUtf8("clicked()")), self.hello_next)
		QtCore.QObject.connect(self.fs, QtCore.SIGNAL(_fromUtf8("clicked()")), self.fullscreen)
		QtCore.QObject.connect(self.line1, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.search)
		QtCore.QObject.connect(self.list3, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setname)
		QtCore.QObject.connect(self.list1, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setchapter1)
		QtCore.QObject.connect(self.list2, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setchapter2)
		QtCore.QObject.connect(self.select, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.selectHistory)
		QtCore.QObject.connect(self.selectSite, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.selectSource)
		"""
		self.nextP.clicked.connect(self.hello_next)
		self.fs.clicked.connect(self.fullscreen)
		self.line1.returnPressed.connect(self.search)
		self.list3.itemDoubleClicked['QListWidgetItem*'].connect(self.setname)
		self.list1.itemDoubleClicked['QListWidgetItem*'].connect(self.setchapter1)
		self.list2.itemDoubleClicked['QListWidgetItem*'].connect(self.setchapter2)
		self.select.currentIndexChanged['int'].connect(self.selectHistory)
		self.selectSite.currentIndexChanged['int'].connect(self.selectSource)
		
		self.scrollArea.verticalScrollBar().valueChanged.connect(self.scrolled)
		###self.scrollArea.verticalScrollBar().actionTriggered.connect(self.scrolled)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.arrow_timer = QtCore.QTimer()
		#self.arrow_timer.connect(self.arrow_timer,QtCore.SIGNAL("timeout()"),self.arrow_hide)
		self.arrow_timer.timeout.connect(self.arrow_hide)
		self.arrow_timer.setSingleShot(True)
		self.prev.hide()
		self.line1.setPlaceholderText("Enter Search Keyword")
		self.downloadWget = []
		self.imgArr = []
		self.downloadWgetUrl = []
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Read Manga", None))
		self.prev.setText(_translate("MainWindow", "Previous", None))
		self.fs.setText(_translate("MainWindow", "FullScreen", None))
		self.nextP.setText(_translate("MainWindow", "Next", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Search", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Chapters", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Page", None))
		self.label2.setText(_translate("MainWindow", "            Page No :", None))
		self.select.setItemText(0, _translate("MainWindow", "Search", None))
		self.select.setItemText(1, _translate("MainWindow", "History", None))
		#self.select.setItemText(2, _translate("MainWindow", "Clear", None))
		self.selectSite.setItemText(0, _translate("MainWindow", "Source", None))
		self.selectSite.setItemText(1, _translate("MainWindow", "KissManga", None))
		self.selectSite.setItemText(2, _translate("MainWindow", "GoodManga", None))
		self.selectSite.setItemText(3, _translate("MainWindow", "MangaBB", None))
		self.selectSite.setItemText(4, _translate("MainWindow", "MangaReader", None))
		self.selectSite.setItemText(5, _translate("MainWindow", "MangaHere", None))
		
		
	def hello_next(self):
		global download,nextp,prevp,picn,chapterNo,pgn,series,downloadNext,pageNo
		t = self.scrollArea.verticalScrollBar().maximum()
		#self.scrollArea.verticalScrollBar().setValue(t)
		if downloadNext == 1:
			pageNo = pageNo+1
			ui.hello(pageNo)
			self.scrollArea.verticalScrollBar().setValue(t)
	def selectSource(self):
		global home,name,site
		self.list3.clear()
		self.list1.clear()
		site = str(self.selectSite.currentText())
		if site != "Source":
			if not os.path.isdir(home+'/'+site):
				os.makedirs(home+'/'+site)
			self.selectHistory()
	def arrow_hide(self):
		self.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
	def selectHistory(self):
		global home,name,options,site
		self.list3.clear()
		self.list1.clear()
		options = str(self.select.currentText())
		if options == "History":
			self.line1.hide()
			if os.path.isdir(home+'/'+site):
				m = os.listdir(home+'/'+site)
				t = home+'/'+site
				m = sorted(m,key= lambda x: os.path.getmtime(t+'/'+x),reverse=True)
				for i in m:
					  i = re.sub('.txt','',i)
					  self.list3.addItem(i)
		elif options == "Clear" or site == "Source":
			self.list3.clear()
			self.line1.show()
		else:
			self.line1.show()
	
    			
	
	
	
    
        
	def scrolled(self,value):
		global download,nextp,prevp,picn,chapterNo,pgn,series,downloadNext,pageNo,screen_height,view_mode
		
		
		if view_mode == 1 or view_mode == 2:
			if value >= self.scrollArea.verticalScrollBar().maximum() - 50:
				#if downloadNext == 1:
				if len(self.downloadWget) == 0:
					pageNo = pageNo+1
					ui.hello(pageNo)
					r = self.list2.currentRow()
					if r < self.list2.count() and r >=0:
						self.list2.setCurrentRow(r+1)
				else:
					val = self.scrollArea.verticalScrollBar().maximum() - 60
					ui.scrollArea.verticalScrollBar().setValue(val)


	def createLabel(self,picN,num):
		global base_url,nextp,prevp,download,nextp_fetched,picn,chapterNo,pgn,series,hdr,arrPage,currentPage,arrReference,downloadNext,label_no,t_ht,arrPage,pageNo,t_width,site,scale_width,scale_height,strict_original,arr_pg_cnt,total_ht,view_mode
		
		arr_pg_cnt.append(label_no)
		
		if label_no > 4 and view_mode == 1:
			#QtGui.QApplication.processEvents()
			#length = len(arr_pg_cnt)
			#while length >= 6:
			pg_del = arr_pg_cnt[0]
			del arr_pg_cnt[0]
			
			try:
				t = "self.label_"+str(pg_del)+".height()"

				ht = eval(t)
				total_ht = total_ht - ht
				print(ht,total_ht,'***********ht vs total_ht cmp*******')
				t = "ui.label_"+str(pg_del)+".deleteLater()"

				exec (t)
				t = "ui.label_text_"+str(pg_del)+".deleteLater()"

				exec (t)
				
				val = self.scrollArea.verticalScrollBar().maximum() - ht - 80
				ui.scrollArea.verticalScrollBar().setValue(val)
				print(total_ht,_ht,'total-height')
			except:
				pass
			"""
			#length = length - 1
			#QtWidgets.QApplication.processEvents()
			if scale_height:
				_ht = 4*scale_height - self.scrollArea.height() + 80
			else:
				if total_ht < 0:
					total_ht = 0
					for i in range(len(arr_pg_cnt)-1):
						t = "self.label_"+str(arr_pg_cnt[i])+".height()"
						ht1 = eval(t)
						print(ht1)
						total_ht = total_ht + ht1
				_ht = total_ht - self.scrollArea.height() + 80
			print(_ht,'--------_ht-------------')
			print(total_ht,_ht,'total-height')
			ui.scrollArea.verticalScrollBar().setValue(_ht)
			"""
		
		
		label_no = num
		#picn = picN
		sz = str(scale_width)+','+str(scale_height)
		p1="self.label_"+str(label_no)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
		  #p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
		p7 = "l_"+str(label_no)+" = weakref.ref(self.label_"+str(label_no)+")"  
		p5="self.label_"+str(label_no)+".setObjectName(_fromUtf8("+'"'+"label_"+str(label_no)+'"'+"))"
		p6="self.horizontalLayout.addWidget(self.label_"+str(label_no)+")"
		#p9 = "self.label_"+str(label_no)+".setMaximumSize(QtCore.QSize(800, 16777215))"
		p9 = "self.label_"+str(label_no)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
		p10 = "self.label_"+str(label_no)+".setMinimumSize(QtCore.QSize("+sz+"))"
		p4="self.label_"+str(label_no)+".setScaledContents(True)"
		p11="self.label_"+str(label_no)+".setMouseTracking(True)"
		p12 = "self.label_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
		
		exec (p1)
		exec (p7)
		exec (p5)
		if not strict_original:
			exec (p9)
			exec (p10)
			exec (p4)
		exec (p6)
		exec (p11)
		exec (p12)
		
		
		
		
		
		picn_t = picN.split('/')[-1]
		
		
	
		p1="self.label_text_"+str(label_no)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
		  #p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
		p7 = "l_text_"+str(label_no)+" = weakref.ref(self.label_text_"+str(label_no)+")"  
		p5="self.label_text_"+str(label_no)+".setObjectName(_fromUtf8("+'"'+"label_text_"+str(label_no)+'"'+"))"
		p6="self.horizontalLayout.addWidget(self.label_text_"+str(label_no)+")"
		p9 = "self.label_text_"+str(label_no)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 100))"
		p4="self.label_text_"+str(label_no)+".setText(picn_t)"
		p2 = "self.label_text_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
		exec (p1)
		exec (p7)
		exec (p5)
		if not strict_original:
			exec (p9)
		exec (p6)
		  
		exec (p4)
		exec (p2)
			
		
		img_err = True
		sz = (0,0)
		try:
			im = Image.open(picN)
			im.verify()
			#im = Image.open(picN)
			sz = im.size
			im.load()
			img_err = False
		except:
			img_err = True
			
		if img_err:
			self.imgArr.append(downloadFile(picN,label_no))
			length = len(self.imgArr)-1
			self.imgArr[length].imgAvailable.connect(imgReadyNew)
			self.imgArr[length].start()
		
		img1 = QtGui.QPixmap(picN, "1")
		p7 = "self.label_"+str(label_no)+".setPixmap(img1)"
		exec (p7)
		#if sz:
		total_ht = total_ht + sz[1]
		print(sz)	
		#print(total_ht,'---total_ht---')
		
		label_no = label_no+1
		
	@pyqtSlot(str,int)
	def imgReady(self,p,n):
		print(len(self.imgArr))
		img1 = QtGui.QPixmap(p, "1")
		p7 = "self.label_"+str(n)+".setPixmap(img1)"
		exec (p7)
		
	def cancelDownload(self):
		if self.downloadWgetNew:
			for i in self.downloadWgetNew:
				if not i.isFinished():
					i.terminate()
			self.downloadWgetNew[:]=[]
		
		if self.downloadWgetUrlNew:
			for i in self.downloadWgetUrlNew:
				if not i.isFinished():
					i.terminate()
			self.downloadWgetUrlNew[:]=[]
			
	def onlyDownload(self):
		global base_url,nextp,prevp,download,nextp_fetched,picn,chapterNo,pgn,series,hdr,arrPage,currentPage,arrReference,downloadNext,label_no,t_ht,arrPage,pageNo,t_width,site
		
		
		
		for i in range(self.list2.count()):
		
			series = name
			try:
				jpgn = (urllib.parse.unquote(arrPage[i])).split('/')[-1]
			except:
				return 0
			jpgn1 = re.sub('.jpg|.png','',jpgn)
			chapterNo_n = chapterNo.split('?')[0] 
			if not chapterNo_n:
					chapterNo_n = chapterNo
			picn = "/tmp/ReadManga/"+name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn1
			
			  
			imgUrl = arrPage[i]
			try:
				pgText = self.list2.item(i).text()
			except:
				pgText = '1.jpg'
				
			if '.jpg' in pgText or '.png' in pgText or '.JPG' in pgText or '.PNG' in pgText:
				command = "wget --user-agent="+'"'+hdr+'" '+arrPage[i]+" -O "+picn
				if os.path.exists(picn):
					img_type = imghdr.what(picn)
				else:
					img_type = 'jpeg'
				if not os.path.exists(picn) or ((os.path.exists(picn) and (img_type!='jpeg' and img_type!='png' and img_type != 'gif'))):
					#self.infoWget(command,picn,label_no)
					self.downloadWgetNew.append(downloadThread(imgUrl+'#'+'-o'+'#'+picn))
					indx = len(self.downloadWgetNew)-1
					self.downloadWgetNew[indx].finished.connect(lambda:self.downloadNew_thread_finished(indx,picn,label_no))
					
				
			#else:
			#	if not os.path.exists(picn):
			#		print('-----download-Url-----')
			#		self.downloadWgetUrlNew.append(downloadUrl(site,name,arrPage[i],picn,label_no))
			#		indxn = len(self.downloadWgetUrlNew)-1
			#		self.downloadWgetUrlNew[indxn].imgUrl.connect(self.downloadUrlNew_thread_finished)
					
		
		if self.downloadWgetNew:
			self.downloadWgetNew[0].start()
		elif self.downloadWgetUrlNew:
			self.downloadWgetUrlNew[0].start()
			
			
		
			
			
		
	@pyqtSlot(str,str,int)
	def downloadUrlNew_thread_finished(self,url,pic,num):
		if url:
			self.downloadWgetNew.append(downloadThread(url+'#'+'-o'+'#'+pic))
			indxn = len(self.downloadWgetNew)-1
			self.downloadWgetNew[indxn].finished.connect(lambda:self.downloadNew_thread_finished(indxn,pic,num))
			self.downloadWgetNew[indxn].start()
		
			
	def downloadNew_thread_finished(self,indx,p,n):
		print(indx,'--indx---')
		print(len(self.downloadWgetNew),'---length---downloadwgetNew')
		#if n == 0:
		#	self.createLabel(p,n)
		#if (indx+1) < len(self.downloadWgetNew):
		#	self.downloadWgetNew[indx+1].start()
		if self.downloadWgetNew:
			del self.downloadWgetNew[0]
			if self.downloadWgetNew:
				self.downloadWgetNew[0].start()
	def hello(self,pageNo_t): 
		global base_url,nextp,prevp,download,nextp_fetched,picn,chapterNo,pgn,series,hdr,arrPage,currentPage,arrReference,downloadNext,label_no,t_ht,arrPage,pageNo,t_width,site
		
		
		#downloadNext = 0
		print (currentPage)
		print (len(arrPage))
		
		val = t_ht+600
		print ("val")
		print (val)
		
		series = name
		try:
			jpgn = (urllib.parse.unquote(arrPage[pageNo_t])).split('/')[-1]
		except:
			return 0
		jpgn1 = re.sub('.jpg|.png','',jpgn)
		chapterNo_n = chapterNo.split('?')[0] 
		if not chapterNo_n:
				chapterNo_n = chapterNo
		picn = "/tmp/ReadManga/"+name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn1
		print (picn)
		self.line2.clear()
		self.line2.insert(str(jpgn1))
		self.line3.clear()
		self.line3.insert("chapter-"+chapterNo_n)
		self.label3.setText(series)
		  
		imgUrl = arrPage[pageNo_t]
		try:
			pgText = self.list2.item(pageNo_t).text()
		except:
			pgText = '1.jpg'
		if '.jpg' in pgText or '.png' in pgText or '.JPG' in pgText or '.PNG' in pgText:
			command = "wget --user-agent="+'"'+hdr+'" '+arrPage[pageNo_t]+" -O "+picn
			if os.path.exists(picn):
				img_type = imghdr.what(picn)
			else:
				img_type = 'jpeg'
			if not os.path.exists(picn) or ((os.path.exists(picn) and (img_type!='jpeg' and img_type!='png' and img_type != 'gif'))):
				#self.infoWget(command,picn,label_no)
				self.downloadWget.append(downloadThread(imgUrl+'#'+'-o'+'#'+picn))
				indx = len(self.downloadWget)-1
				self.downloadWget[indx].finished.connect(lambda:self.download_thread_finished(indx,picn,label_no))
				self.downloadWget[indx].start()
			
		else:
			if not os.path.exists(picn):
				print('-----download-Url-----')
				self.downloadWgetUrl.append(downloadUrl(site,name,arrPage[pageNo_t],picn,label_no))
				indxn = len(self.downloadWgetUrl)-1
				self.downloadWgetUrl[indxn].imgUrl.connect(downloadUrl_thread_finished)
				self.downloadWgetUrl[indxn].start()
			
		self.createLabel(picn,label_no)
			
		
			
			
		
		#downloadNext = 1
		if pageNo_t+1 < len(arrPage): 
			#jpgn_n = (arrPage[pageNo_t+1].split('/')[-1])
			jpgn_n = (urllib.parse.unquote(arrPage[pageNo_t+1])).split('/')[-1]
			jpgn_n = re.sub('.jpg|.png','',jpgn_n)
			chapterNo_n = chapterNo.split('?')[0]
			if not chapterNo_n:
				chapterNo_n = chapterNo 
			picn1 = "/tmp/ReadManga/" + name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn_n
			pgText = self.list2.item(pageNo_t+1).text()
			imgUrl1 = arrPage[pageNo_t+1]
			if '.jpg' in pgText or '.png' in pgText or '.JPG' in pgText or '.PNG' in pgText:
				command1 = "wget --user-agent="+'"'+hdr+'" '+arrPage[pageNo_t+1]+" -O "+picn1
				if os.path.exists(picn1):
					img_type = imghdr.what(picn1)
				else:
					img_type = 'jpeg'
					
				
				if not os.path.exists(picn1) or ((os.path.exists(picn1) and (img_type!='jpeg' and img_type!='png' and img_type != 'gif'))):
					self.downloadWget.append(downloadThread(imgUrl1+'#'+'-o'+'#'+picn1))
					indxn = len(self.downloadWget)-1
					self.downloadWget[indxn].finished.connect(lambda:self.download_thread_finished(indxn,picn1,label_no+1))
					self.downloadWget[indxn].start()
			else:
				if not os.path.exists(picn1):
					print('-----download-Url-----')
					self.downloadWgetUrl.append(downloadUrl(site,name,arrPage[pageNo_t+1],picn1,label_no + 1))
					indxn = len(self.downloadWgetUrl)-1
					self.downloadWgetUrl[indxn].imgUrl.connect(downloadUrl_thread_finished)
					self.downloadWgetUrl[indxn].start()
			
			
			
			
		else:
			row = self.list1.currentRow()
			if (row+1) < self.list1.count():
				self.list1.setCurrentRow(row+1)
			else:
				self.list1.setCurrentRow(0)
			pageNo = -1
			#label_no = 0
			nam = self.list1.currentItem().text()
			nam = str(nam)
			chapterNo = nam
			chapterNo_n = chapterNo.split('?')[0] 
			if not chapterNo_n:
				chapterNo_n = chapterNo
			ka=Manga_Read(site)
			nxt=ka.getPage(site,name,nam)
			del ka
			self.list2.clear()
			arrPage[:]=[]
			for i in nxt:
				arrPage.append(i)
				self.list2.addItem(i.split('/')[-1])
			imgUrl1 = arrPage[0]
			#jpgn_n = (arrPage[0].split('/')[-1])
			jpgn_n = (urllib.parse.unquote(arrPage[0])).split('/')[-1]
			jpgn_n = re.sub('.jpg|.png','',jpgn_n)
			picn1 = "/tmp/ReadManga/" + name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn_n
			pgText = self.list2.item(0).text()
			if '.jpg' in pgText or '.png' in pgText or '.JPG' in pgText or '.PNG' in pgText:
				command1 = "wget --user-agent="+'"'+hdr+'" '+arrPage[0]+" -O "+picn1
				if os.path.exists(picn1):
					img_type = imghdr.what(picn1)
				else:
					img_type = 'jpeg'
					
				
				if not os.path.exists(picn1) or ((os.path.exists(picn1) and (img_type!='jpeg' and img_type!='png' and img_type != 'gif'))):
					self.downloadWget.append(downloadThread(imgUrl1+'#'+'-o'+'#'+picn1))
					indxn = len(self.downloadWget)-1
					self.downloadWget[indxn].finished.connect(lambda:self.download_thread_finished(indxn,picn1,label_no+1))
					self.downloadWget[indxn].start()
			else:
				if not os.path.exists(picn1):
					print('-----download-Url-----')
					self.downloadWgetUrl.append(downloadUrl(site,name,arrPage[0],picn1,label_no + 1))
					indxn = len(self.downloadWgetUrl)-1
					self.downloadWgetUrl[indxn].imgUrl.connect(downloadUrl_thread_finished)
					self.downloadWgetUrl[indxn].start()
			
			
			
	#@pyqtSlot(str,str,int)
	#def downloadUrl_thread_finished(self,url,pic,num):
	#	if url:
	#		self.downloadWget.append(downloadThread(url+'#'+'-o'+'#'+pic))
	#		indxn = len(self.downloadWget)-1
	#		self.downloadWget[indxn].finished.connect(lambda:self.download_thread_finished(indxn,pic,num))
	#		self.downloadWget[indxn].start()
	#	else:
	#		self.createLabel(pic,num)
			
	def download_thread_finished(self,indx,p,n):
		print(indx,'--indx---')
		print(len(self.downloadWget),'---length---downloadwget')
		#if n == 0:
		#	self.createLabel(p,n)
		if self.downloadWget:
			try:
				#if self.downloadWget[indx].isFinished():
				#	del self.downloadWget[indx]
				r = 0
				for i in self.downloadWget:
					if i:
						if i.isFinished():
							del self.downloadWget[r]
					r = r+1
			except:
				r = 0
				for i in self.downloadWget:
					if i:
						if i.isFinished():
							del self.downloadWget[r]
					r = r+1
				#self.downloadWget[:]=[]
				print('index-error')
	
	def fullscreen(self):
		global fullscr
		if not MainWindow.isFullScreen():
			MainWindow.showFullScreen()
			fullscr = 1
			self.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
			self.frame.hide()
			self.dockWidget.hide()
		else:
			MainWindow.showMaximized()
			fullscr = 0
			self.scrollArea.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.frame.show()
			self.dockWidget.show()
	def normal(self):
		MainWindow.showNormal()

	def search(self):
		global name,m_no,site
		srch = str(self.line1.text())
		ka = Manga_Read(site)
		nxt = ka.search(site,srch)
		del ka
		self.list3.clear()
		self.list1.clear()
		for i in nxt:
			self.list3.addItem(i)
	  
	def setname(self):
		global name,download,home,options,pre_name,arrPage,arrReference,currentPage,chapterNo,pageNo,label_no,site,arr_pg_cnt,total_ht
		if self.downloadWget:
			for i in self.downloadWget:
				if not i.isFinished():
					i.terminate()
			self.downloadWget[:]=[]
		index = 0
		m = os.listdir('/tmp/ReadManga/')
		for i in m:
			if '.jpg' in i:
				t = '/tmp/ReadManga/'+i
				os.remove(t)
		
		if os.path.exists(home+"/"+site+'/'+name+".txt"):
			f = open(home+"/"+site+'/'+name+".txt", "w")
			f.write(name+':'+chapterNo+":"+str(ui.list1.currentRow())+":"+str(pageNo))
			f.close()
		i = 0
		while(i<label_no):
			try:
				t = "ui.label_"+str(i)+".deleteLater()"

				exec (t)
				t = "ui.label_text_"+str(i)+".deleteLater()"

				exec (t)
			except:
				pass
			i = i+1
		label_no = 0
		arr_pg_cnt[:]=[]
		total_ht = 0
		name = self.list3.currentItem().text()
		name = str(name)
		download = 0
		print (name)
		ka = Manga_Read(site)
		m = ka.getInfo(site,name)
		del ka
		if m:
			m.pop()
			m.pop()
		self.list1.clear()
		for i in m:
			self.list1.addItem(i)
		if options == "History":
			if os.path.isfile(home+"/"+site+'/'+name+".txt"):
				lines = tuple(open(home+'/'+site+'/'+name+".txt", 'r'))
				if lines:
					base_url = str(lines[0]).split(':')
					name = base_url[0]
					chapterNo = base_url[1]
					length = self.list1.count()
					i = 0
					while(i<length):
						t = str(self.list1.item(i).text())
						if chapterNo == t:
							index = i
							break
						i = i+1
					if not index:
						index = int(base_url[2])
					
					self.list1.setCurrentRow(index)
					self.getEpnInfo()
					pageNo = int(base_url[3])
					#label_no = pageNo
					self.list2.setCurrentRow(pageNo)
					self.setchapter2()
				
		else:
			
			
			if not os.path.isfile(home+"/"+site+'/'+name+".txt"):
				self.list1.setCurrentRow(0)
				self.getEpnInfo()
				self.list2.setCurrentRow(0)
				self.setchapter2()
				f = open(home+"/"+site+'/'+name+".txt", "w")
				f.write(name+':'+chapterNo+":"+str(ui.list1.currentRow())+":"+str(pageNo))
				f.close()
				
    
	
	def setchapter1(self):
		global name,base_url,chapterNo,nam,arrPage,pageNo,label_no,site,arr_pg_cnt,total_ht
		pageNo = 0
		#label_no = pageNo
		i = 0
		while(i<label_no):
			try:
				t = "ui.label_"+str(i)+".deleteLater()"

				exec (t)
				t = "ui.label_text_"+str(i)+".deleteLater()"

				exec (t)
			except:
				pass
			i = i+1
		label_no = 0
		arr_pg_cnt[:]=[]
		total_ht = 0
		nam = self.list1.currentItem().text()
		nam = str(nam)
		chapterNo = nam
		ka=Manga_Read(site)
		nxt=ka.getPage(site,name,nam)
		del ka
		self.list2.clear()
		arrPage[:]=[]
		for i in nxt:
			arrPage.append(i)
			self.list2.addItem(i.split('/')[-1])
		ui.hello(pageNo)
	
	def getEpnInfo(self):
		global name,base_url,chapterNo,nam,arrPage,pageNo,site
		try:
			pageNo = 0
			nam = self.list1.currentItem().text()
			nam = str(nam)
			chapterNo = nam
			
			ka=Manga_Read(site)
			nxt=ka.getPage(site,name,nam)
			del ka
			self.list2.clear()
			arrPage[:]=[]
			for i in nxt:
				arrPage.append(i)
				self.list2.addItem(i.split('/')[-1])
			print (arrPage)
		except:
			pass
	  
	def setchapter2(self):
		global name,base_url,chapterNo,nam,arrPage,pageNo,label_no,arr_pg_cnt,total_ht
		i = 0
		while(i<label_no):
			try:
				t = "ui.label_"+str(i)+".deleteLater()"

				exec (t)
				t = "ui.label_text_"+str(i)+".deleteLater()"

				exec (t)
			except:
				pass
			i = i+1
		label_no = 0
		arr_pg_cnt[:]=[]
		total_ht = 0
		pageNo = self.list2.currentRow()
		#label_no = pageNo
		self.hello(pageNo)
		self.scrollArea.verticalScrollBar().setValue(0)

	




if __name__ == "__main__":
	import sys
	global base_url,download,nextp_fetched,fullscr,wget,hdr,home,options,name,pre_name,pgn,currentPage,arrPage,arrReference,downloadNext,label_no,t_ht,t_width,scale_width,screen_width,screen_height,view_mode,scale_height,strict_original,arr_pg_cnt,site,total_ht
	strict_original = False
	site = ''
	total_ht = 0
	arr_pg_cnt = []
	view_mode = 1
	scale_width = 900
	scale_height = 0
	t_width=900
	chapterNo = ""
	t_ht = 0
	label_no = 0
	downloadNext = 0
	currentPage = 0
	arrReference = []
	arrPage = []
	pgn = "1.jpg"
	pre_name = ""
	name = ""
	options =""
	pageNo = 0
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0"
	fullscr = 0
	nextp_fetched = 0
	download = 0
	base_url = ""
	wget = ""
	site = ''
	home = expanduser("~")
	home = home+"/.config/ReadMangaKA"
	app = QtWidgets.QApplication(sys.argv)
	#MainWindow = QtGui.QMainWindow()
	MainWindow = QtWidgets.QWidget()
	screen_resolution = app.desktop().screenGeometry()
	screen_width = screen_resolution.width()
	screen_height = screen_resolution.height()
	print (screen_height,screen_width)
	
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	if not os.path.exists(home):
		os.makedirs(home)
	if not os.path.exists(home+'/config.txt'):
		f = open(home+'/config.txt','w')
		f.write('scale_width=0'+'\n'+'scale_height=0'+'\n'+'view_mode=1')
		f.close()
	if not os.path.exists('/tmp/ReadManga/'):
		os.makedirs('/tmp/ReadManga/')
	if os.path.exists(home+'/src'):
		os.chdir(home+'/src')
		sys.path.append(home+'/src')
	try:
		m = os.listdir('/tmp/ReadManga/')
		for i in m:
			if '.jpg' in i or '.png' in i:
				t = '/tmp/ReadManga/'+i
				os.remove(t)
	
	except:
		pass

	try:
		if os.path.exists(home+'/config.txt'):
			f = open(home+'/config.txt','r')
			lines = f.readlines()
			f.close()
			for i in lines:
				i = i.replace('\n','')
				j = i.split('=')
				if j[0] == 'scale_width':
					scale_width = int(float(j[1]))
				elif j[0] == 'scale_height':
					scale_height = int(float(j[1]))
				elif j[0] == 'view_mode':
					view_mode = int(float(j[1]))
			
	except:
		scale_width = 0
		scale_height = 0
		view_mode = 1
		
	
	if not scale_width:
		scale_height = 0
		strict_original = True
	MainWindow.show()
	ui.scrollArea.setStyleSheet("font:bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
	ret = app.exec_()

	if os.path.isfile(home+"/"+site+"/"+name+".txt"):
		if site:
			f = open(home+"/"+site+"/"+name+".txt", "w")
			if pageNo == -1:
				row = ui.list1.currentRow()-1
				chapterNo = str(ui.list1.item(row).text())
				f.write(name+':'+chapterNo+":"+str(row)+":"+str(pageNo))
			else:
				f.write(name+':'+chapterNo+":"+str(ui.list1.currentRow())+":"+str(pageNo))
			f.close()
		
		f = open(home+'/config.txt','w')
		f.write('scale_width='+str(int(scale_width))+'\n'+'scale_height='+str(int(scale_height))+'\n'+'view_mode='+str(int(view_mode)))
		f.close()
		
		if ui.downloadWget:
			for i in ui.downloadWget:
				if not i.isFinished():
					i.terminate()
			ui.downloadWget[:]=[]
			
		if ui.imgArr:
			for i in ui.imgArr:
				if not i.isFinished():
					i.terminate()
			ui.imgArr[:]=[]
		
		if ui.downloadWgetUrl:
			for i in ui.downloadWgetUrl:
				if not i.isFinished():
					i.terminate()
			ui.downloadWgetUrl[:]=[]
	del app
	sys.exit(ret)

