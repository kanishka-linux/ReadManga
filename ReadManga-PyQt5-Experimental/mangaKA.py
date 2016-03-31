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
from functools import partial
from os.path import expanduser
from Manga_Read import Manga_Read
import weakref

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
		epn=eval(p7)
		print (epn)
		
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
			
		else:
			subprocess.Popen(["killall","wget"])
			ep1 = picn.split('-')[-1]
			if '.html' in ep1:
				ep = ep1
			else:
				ep = ep1+'.jpg'
			length = ui.list2.count()
			i = 0
			while i < length:
				print (ep + ":"+ui.list2.item(i).text())
				if str(ui.list2.item(i).text()) == str(ep):
					index = i
					break
				i = i+1
			#subprocess.Popen(["wget","--user-agent="+'"'+hdr+'"',arrPage[num],"-O",picn])
			print (arrPage[index])
			print ("downloading")
			#command = "wget --user-agent="+'"'+hdr+'" '+arrPage[index]+" -O "+picn
			#ui.infoWget(command)
			pgText = ui.list2.item(index).text()
			if '.jpg' in pgText or '.png' in pgText:
				subprocess.Popen(["wget", "-c","--user-agent="+'"'+hdr+'"',arrPage[index],"-O",picn])
			else:
				ka = Manga_Read(site)
				imgUrl = ka.getPageImg(site,name,arrPage[index]) 
				del ka
				subprocess.Popen(["wget","-c","--user-agent="+'"'+hdr+'"',imgUrl,"-O",picn])
			
		
		QtWidgets.QApplication.processEvents()
		
	

class MyScrollArea(QtWidgets.QScrollArea):
	def __init__(self, parent):
		super(MyScrollArea, self).__init__(parent)
		global frame_toggle
		frame_toggle = 0
	
	def keyPressEvent(self, event):
		global frame_toggle,name,label_no,chapterNo,arrPage,pageNo,label_no,t_width,scale_width
		if event.key() == QtCore.Qt.Key_Right:
		    ui.hello(pageNo)
		elif event.key() == QtCore.Qt.Key_W:
			t_width = str(self.width())
			print (t_width)
			for i in range(label_no):
				p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 16777215))"
				p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+str(t_width)+", 0))"
				exec (p9)
				exec (p10)
		elif event.key() == QtCore.Qt.Key_O:
			t_width = str(900)
			print (t_width)
			for i in range(label_no):
				p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 16777215))"
				p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+str(t_width)+", 0))"
				exec (p9)
				exec (p10)
		elif event.key() == QtCore.Qt.Key_Equal:
			scale_width = scale_width + (scale_width * 0.1)
			t_width = scale_width
			for i in range(label_no):
				p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
				p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+str(scale_width)+", 0))"
				exec (p9)
				exec (p10)
		elif event.key() == QtCore.Qt.Key_Minus:
			scale_width = scale_width - (scale_width * 0.1)
			t_width = scale_width
			for i in range(label_no):
				p9 = "ui.label_"+str(i)+".setMaximumSize(QtCore.QSize("+str(scale_width)+", 16777215))"
				p10 = "ui.label_"+str(i)+".setMinimumSize(QtCore.QSize("+str(scale_width)+", 0))"
				exec (p9)
				exec (p10)
		elif event.key() == QtCore.Qt.Key_Left:
			pageNo = pageNo - 1
			ui.hello(pageNo)
		elif event.key() == QtCore.Qt.Key_F:
			ui.fullscreen()
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

def ccurl(url):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0"
	c = pycurl.Curl()
	c.setopt(c.USERAGENT, hdr)
	url = str(url)
	c.setopt(c.URL, url)
	storage = StringIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	return content

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
		self.next = QtWidgets.QPushButton(self.frame)
		self.next.setObjectName(_fromUtf8("next"))
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
		self.gridLayout.addWidget(self.next, 0, 5, 1, 1, QtCore.Qt.AlignRight)
		self.gridLayout.addWidget(self.fs, 0, 6, 1, 1, QtCore.Qt.AlignRight)
		self.gridLayout.addWidget(self.progress,0,7,1,1)
		self.horizontalLayout.setAlignment(QtCore.Qt.AlignCenter)
		#self.nxtp = QtGui.QAction(self)
		QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self.frame, self.hello_next)
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
		QtCore.QObject.connect(self.next, QtCore.SIGNAL(_fromUtf8("clicked()")), self.hello_next)
		QtCore.QObject.connect(self.fs, QtCore.SIGNAL(_fromUtf8("clicked()")), self.fullscreen)
		QtCore.QObject.connect(self.line1, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.search)
		QtCore.QObject.connect(self.list3, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setname)
		QtCore.QObject.connect(self.list1, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setchapter1)
		QtCore.QObject.connect(self.list2, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.setchapter2)
		QtCore.QObject.connect(self.select, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.selectHistory)
		QtCore.QObject.connect(self.selectSite, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.selectSource)
		"""
		self.next.clicked.connect(self.hello_next)
		self.fs.clicked.connect(self.fullscreen)
		self.line1.returnPressed.connect(self.search)
		self.list3.itemDoubleClicked['QListWidgetItem*'].connect(self.setname)
		self.list1.itemDoubleClicked['QListWidgetItem*'].connect(self.setchapter1)
		self.list2.itemDoubleClicked['QListWidgetItem*'].connect(self.setchapter2)
		self.select.currentIndexChanged['int'].connect(self.selectHistory)
		self.selectSite.currentIndexChanged['int'].connect(self.selectSource)
		
		self.scrollArea.verticalScrollBar().valueChanged.connect(self.scrolled)
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
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Read Manga", None))
		self.prev.setText(_translate("MainWindow", "Previous", None))
		self.fs.setText(_translate("MainWindow", "FullScreen", None))
		self.next.setText(_translate("MainWindow", "Next", None))
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
		self.selectSite.setItemText(3, _translate("MainWindow", "MangaHere", None))
		self.selectSite.setItemText(4, _translate("MainWindow", "MangaBB", None))
		self.selectSite.setItemText(5, _translate("MainWindow", "MangaReader", None))
	def hello_next(self):
		global download,nextp,prevp,picn,chapterNo,pgn,series,downloadNext,pageNo
		t = self.scrollArea.verticalScrollBar().maximum()
		self.scrollArea.verticalScrollBar().setValue(t)
		if downloadNext == 1:
			pageNo = pageNo+1
			ui.hello(pageNo)
	def selectSource(self):
		global home,name,site
		self.list3.clear()
		self.list1.clear()
		site = str(self.selectSite.currentText())
		if site != "Source":
			if not os.path.isdir(home+'/'+site):
				os.makedirs(home+'/'+site)
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
				for i in m:
					  i = re.sub('.txt','',i)
					  self.list3.addItem(i)
		elif options == "Clear" or site == "Source":
			self.list3.clear()
			self.line1.show()
		else:
			self.line1.show()
	def dataReadyW(self,p):
		global wget,new_epn,quitReally,curR,epn,opt,base_url,Player,site,sizeFile
		#wget.waitForReadyRead()
		try:
			a = str(p.readAllStandardOutput()).strip()
			#print a
			if "Length:" in a:
				l = re.findall('[(][^)]*[)]',a)
				if l:
					sizeFile = l[0]
			if "%" in a:
				m = re.findall('[0-9][^\n]*',a)
				if m:
					#print m[0]
					n = re.findall('[^%]*',m[0])
					if n:
						val = int(n[0])
						self.progress.setValue(val)
					out = str(m[0])+" "+sizeFile +"(Loading Page Wait!)"
					#self.goto_epn.setText(out)
					self.progress.setFormat(out)
		except:
			pass
	
    			
	def startedW(self):
		global download
		#if download == 0:
		#self.frame.show()
		self.progress.setValue(0)
		self.progress.show()
		print ("Process Started")
			
	
	def finishedW(self):
		global picn,downloadNext,arrPage,t_ht,label_no,name,pageNo,chapterNo,t_width
		#if download == 0:
		#arrPage.append(picn)
		#downloadNext = 0
		self.progress.setValue(100)
		self.progress.hide()
		#self.frame.hide()
		img1 = QtGui.QPixmap(picn, "1")
		p7 = "self.label_"+str(label_no)+".setPixmap(img1)"
		exec (p7)
		p8 = "self.label_"+str(label_no)+".height()"
		l_ht = eval (p8)
		p11 = "self.label_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
		exec (p11)
		if pageNo != -1 and pageNo < self.list2.count():
			series = name
			#jpgn = (arrPage[pageNo].split('/')[-1])
			#pgn = jpgn.split(".")[0]
			  
			jpgn = (urllib.parse.unquote(arrPage[pageNo])).split('/')[-1] 
			
			
			jpgn1 = re.sub('.jpg|.png','',jpgn)
			chapterNo_n = chapterNo.split('?')[0]
			if not chapterNo_n:
				chapterNo_n = chapterNo
			picn_t = name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn1
			
			p1="self.label_text_"+str(label_no)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
			  #p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
			p7 = "l_text_"+str(label_no)+" = weakref.ref(self.label_text_"+str(label_no)+")" 
			p5="self.label_text_"+str(label_no)+".setObjectName(_fromUtf8("+'"'+"label_text_"+str(label_no)+'"'+"))"
			p6="self.horizontalLayout.addWidget(self.label_text_"+str(label_no)+")"
			p9 = "self.label_text_"+str(label_no)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 100))"
			p4="self.label_text_"+str(label_no)+".setText(picn_t)"
			p2 = "self.label_text_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
			exec (p1)
			exec (p7)
			exec (p5)
			exec (p9)
			exec (p6)
			  
			exec (p4)
			exec (p2)
		
		print (l_ht)
		t_ht = self.scrollAreaWidgetContents.height()
		print (t_ht)
		downloadNext  = 1
		label_no = label_no+1
			#img1 = QtGui.QPixmap(picn, "1")
			#self.label.setPixmap(img1)
		#QtGui.QApplication.processEvents()


	def infoWget(self,command):
		global wget

		wget = QtCore.QProcess()
		wget.setProcessChannelMode(QtCore.QProcess.MergedChannels)


		wget.started.connect(self.startedW)
		wget.readyReadStandardOutput.connect(partial(self.dataReadyW,wget))
		#self.tab_5.setFocus()
		wget.finished.connect(self.finishedW)
		QtCore.QTimer.singleShot(1000, partial(wget.start, command))   
	  
	  
	  
	def ReadyWN(self,p):
		global wgetN,new_epn,quitReally,curR,epn,opt,base_url,Player,site,sizeFile
		print ("downloading wgetn")
		  
	
			
	def startedWN(self):
	
		#self.progress.setValue(0)
		#self.progress.show()
		print ("Process wgetn Started")
		
	
	def finishedWN(self):
		global picn,pgn,chapterNo,download,nextp,prevp,series,wgetN,arrReference,arrPage,currentPage
		
		#self.progress.setValue(100)
		self.progress.hide()
		print ("Process wgetn finished")
	
	
	
	def getNextScrolledPage(self,command):
		global wgetN
		  
		wgetN = QtCore.QProcess()
		#wgetN.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		  
		  
		wgetN.started.connect(self.startedWN)
		wgetN.readyReadStandardOutput.connect(partial(self.ReadyWN,wgetN))
		#self.tab_5.setFocus()
		wgetN.finished.connect(self.finishedWN)
		QtCore.QTimer.singleShot(1000, partial(wgetN.start, command))
	  
    
        
	def scrolled(self,value):
		global download,nextp,prevp,picn,chapterNo,pgn,series,downloadNext,pageNo
		
		
		if value == self.scrollArea.verticalScrollBar().maximum():
			if downloadNext == 1:
				pageNo = pageNo+1
				ui.hello(pageNo)
	



	def hello(self,pageNo_t): 
		global base_url,nextp,prevp,download,nextp_fetched,picn,chapterNo,pgn,series,hdr,arrPage,currentPage,arrReference,downloadNext,label_no,t_ht,arrPage,pageNo,t_width,site
		
		try:
			downloadNext = 0
			print (currentPage)
			print (len(arrPage))
			
			val = t_ht+600
			print ("val")
			print (val)
			#self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().minimum())
			#self.scrollArea.verticalScrollBar().setValue(int(val))
			
			series = name
			#jpgn = (arrPage[pageNo_t].split('/')[-1]) 
			jpgn = (urllib.parse.unquote(arrPage[pageNo_t])).split('/')[-1]
			  #pgn = jpgn.split(".")[0]
			jpgn1 = re.sub('.jpg|.png','',jpgn)
			chapterNo_n = chapterNo.split('?')[0] 
			if not chapterNo_n:
					chapterNo_n = chapterNo
			#picn = "/tmp/ReadManga/" + name + '-' + "chapter-" + chapterNo + "-page-" + jpgn
			picn = "/tmp/ReadManga/"+name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn1
			print (picn)
			self.line2.clear()
			self.line2.insert(str(jpgn1))
			self.line3.clear()
			self.line3.insert("chapter-"+chapterNo_n)
			self.label3.setText(series)
			  
			p1="self.label_"+str(label_no)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
			  #p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
			p7 = "l_"+str(label_no)+" = weakref.ref(self.label_"+str(label_no)+")"  
			p5="self.label_"+str(label_no)+".setObjectName(_fromUtf8("+'"'+"label_"+str(label_no)+'"'+"))"
			p6="self.horizontalLayout.addWidget(self.label_"+str(label_no)+")"
			#p9 = "self.label_"+str(label_no)+".setMaximumSize(QtCore.QSize(800, 16777215))"
			p9 = "self.label_"+str(label_no)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 16777215))"
			p10 = "self.label_"+str(label_no)+".setMinimumSize(QtCore.QSize("+str(t_width)+", 0))"
			p4="self.label_"+str(label_no)+".setScaledContents(True)"
			p11="self.label_"+str(label_no)+".setMouseTracking(True)"
			p12 = "self.label_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
			
			exec (p1)
			exec (p7)
			exec (p5)
			exec (p9)
			exec (p10)
			exec (p6)
			exec (p11)
			exec (p4)
			exec (p12)
			pgText = self.list2.item(pageNo_t).text()
			if '.jpg' in pgText or '.png' in pgText:
				command = "wget --user-agent="+'"'+hdr+'" '+arrPage[pageNo_t]+" -O "+picn
			else:
				ka = Manga_Read(site)
				imgUrl = ka.getPageImg(site,name,arrPage[pageNo_t]) 
				del ka
				command = "wget --user-agent="+'"'+hdr+'" '+imgUrl+" -O "+picn
			#command = "wget --user-agent="+'"'+hdr+'" '+arrPage[pageNo_t]+" -O "+picn
			if not os.path.exists(picn):
				self.infoWget(command)
			else:
				img1 = QtGui.QPixmap(picn, "1")
				p7 = "self.label_"+str(label_no)+".setPixmap(img1)"
				exec (p7)
				p8 = "self.label_"+str(label_no)+".height()"
				l_ht= eval(p8)
				
				picn_t = name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn1
			
				p1="self.label_text_"+str(label_no)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
				  #p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
				p7 = "l_text_"+str(label_no)+" = weakref.ref(self.label_text_"+str(label_no)+")"  
				p5="self.label_text_"+str(label_no)+".setObjectName(_fromUtf8("+'"'+"label_text_"+str(label_no)+'"'+"))"
				p6="self.horizontalLayout.addWidget(self.label_text_"+str(label_no)+")"
				p9 = "self.label_text_"+str(label_no)+".setMaximumSize(QtCore.QSize("+str(t_width)+", 100))"
				p4="self.label_text_"+str(label_no)+".setText(picn_t)"
				p2 = "self.label_text_"+str(label_no)+".setAlignment(QtCore.Qt.AlignCenter)"
				exec (p1)
				exec (p7)
				exec (p5)
				exec (p9)
				exec (p6)
				  
				exec (p4)
				exec (p2)
				
				print (l_ht)
				t_ht = self.scrollAreaWidgetContents.height()
				print (t_ht)
				
				downloadNext = 1
				label_no = label_no+1
				
			if pageNo_t+1 < len(arrPage): 
				#jpgn_n = (arrPage[pageNo_t+1].split('/')[-1])
				jpgn_n = (urllib.parse.unquote(arrPage[pageNo_t+1])).split('/')[-1]
				jpgn_n = re.sub('.jpg|.png','',jpgn_n)
				chapterNo_n = chapterNo.split('?')[0]
				if not chapterNo_n:
					chapterNo_n = chapterNo 
				picn1 = "/tmp/ReadManga/" + name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn_n
				pgText = self.list2.item(pageNo_t+1).text()
				if '.jpg' in pgText or '.png' in pgText:
					command1 = "wget --user-agent="+'"'+hdr+'" '+arrPage[pageNo_t+1]+" -O "+picn1
				else:
					ka = Manga_Read(site)
					imgUrl = ka.getPageImg(site,name,arrPage[pageNo_t+1]) 
					del ka
					command1 = "wget --user-agent="+'"'+hdr+'" '+imgUrl+" -O "+picn1
				if not os.path.exists(picn1):
					self.getNextScrolledPage(command1)
			else:
				row = self.list1.currentRow()
				self.list1.setCurrentRow(row+1)
				pageNo = -1
				#label_no = 0
				if self.list1.currentItem():
					nam = self.list1.currentItem().text()
				else:
					self.list1.setCurrentRow(0)
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
				#jpgn_n = (arrPage[0].split('/')[-1])
				jpgn_n = (urllib.parse.unquote(arrPage[0])).split('/')[-1]
				jpgn_n = re.sub('.jpg|.png','',jpgn_n)
				picn1 = "/tmp/ReadManga/" + name + '-' + "chapter-" + chapterNo_n + "-page-" + jpgn_n
				pgText = self.list2.item(0).text()
				if '.jpg' in pgText or '.png' in pgText:
					command1 = "wget --user-agent="+'"'+hdr+'" '+arrPage[0]+" -O "+picn1
				else:
					ka = Manga_Read(site)
					imgUrl = ka.getPageImg(site,name,arrPage[0]) 
					del ka
					command1 = "wget --user-agent="+'"'+hdr+'" '+imgUrl+" -O "+picn1
				#command1 = "wget --user-agent="+'"'+hdr+'" '+arrPage[0]+" -O "+picn1
				if not os.path.exists(picn1):
					self.getNextScrolledPage(command1)
		except:
			pass
		#QtGui.QApplication.processEvents()
		

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
		global name,download,home,options,pre_name,arrPage,arrReference,currentPage,chapterNo,pageNo,label_no,site
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
		global name,base_url,chapterNo,nam,arrPage,pageNo,label_no,site
		pageNo = 0
		#label_no = pageNo
		i = 0
		while(i<label_no):
			t = "ui.label_"+str(i)+".deleteLater()"

			exec (t)
			t = "ui.label_text_"+str(i)+".deleteLater()"

			exec (t)
			i = i+1
		label_no = 0
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
		global name,base_url,chapterNo,nam,arrPage,pageNo,label_no
		pageNo = self.list2.currentRow()
		#label_no = pageNo
		ui.hello(pageNo)
		
	




if __name__ == "__main__":
	import sys
	global base_url,download,nextp_fetched,fullscr,wget,hdr,home,options,name,pre_name,pgn,currentPage,arrPage,arrReference,downloadNext,label_no,t_ht,t_width,scale_width
	scale_width = 900
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
	home = expanduser("~")
	home = home+"/.config/ReadMangaKA"
	app = QtWidgets.QApplication(sys.argv)
	#MainWindow = QtGui.QMainWindow()
	MainWindow = QtWidgets.QWidget()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	if not os.path.exists(home):
		os.makedirs(home)
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

	MainWindow.show()
	ret = app.exec_()

	if os.path.isfile(home+"/"+site+"/"+name+".txt"):
		f = open(home+"/"+site+"/"+name+".txt", "w")
		if pageNo == -1:
			row = ui.list1.currentRow()-1
			chapterNo = str(ui.list1.item(row).text())
			f.write(name+':'+chapterNo+":"+str(row)+":"+str(pageNo))
		else:
			f.write(name+':'+chapterNo+":"+str(ui.list1.currentRow())+":"+str(pageNo))
		f.close()
	sys.exit(ret)

