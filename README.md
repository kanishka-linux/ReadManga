#ReadManga :  A GNU/Linux Desktop Application for reading Japanese Manga from various sites available on the internet

Note: This application fetches manga images from various sites available on the internet.
Therefore, before using this application please check the copyright and licensing laws of your country. Because it's possible that some of these Manga might be already licensed in your country. Therefore use this application at your own risk. Author of the 'ReadManga' application is not at all related to any of these sites or their content provider. This application is simply a desktop client that fetches manga images from sites on the internet. If the site from which this application fetches images either closes or changes it's source, then this application will also fail to perform it's designated function. 

#Screenshot
![ReadManga](/Images/sample.png)

#Dependencies and Installation:
(ReadManga Application is mainly written in pyqt4 and python3)
(ReadManga-PyQt5 Application is experimental and written in pyqt5 and python3)

Note: If you've successfully installed AnimeWatch Player before, then you don't have to install any dependencies at all and can directly go to main installation process.

python3

python-pyqt4 {for stable ReadManga Application}

python-pyqt5 (for experimental ReadManga-PyQt5 Application)

python-requests

python-urllib3

python-pillow

python-beautifulsoup4

python-lxml

python-pip

python-pycurl

python-psutil

curl

wget

phantomjs

#Dependencies installation in arch.

sudo pacman -S python python-pyqt4 python-pyqt5 python-pycurl python-requests python-urllib3 python-pillow python-beautifulsoup4 python-lxml python-psutil python-pip curl wget phantomjs



#In ubuntu 14.04, default python points to python 2.7, hence for installing dependencies use following command

sudo apt-get install python3 python3-pyqt4 python3-pyqt5 python3-pycurl python3-requests python3-urllib3 python3-pil python3-bs4 python3-lxml python3-psutil python3-pip curl wget phantomjs



#Once Dependencies are installed Download the folder. Goto ReadManga Directory containing 'install.py' file (If you want stable version of the application written in pyqt4). If you want to try experimental version of the application written in pyqt5 then goto ReadManga-PyQt5 Directory containing 'install.py' file. 
Once you are inside the required directory, Open Terminal in the directory and use following command:

#In Arch:

python install.py

#In Ubuntu 14.04:

python3 install.py

Application Launcher will be created as "~/.local/share/applications/readmanga.desktop"

All other configuration files will be created in "~/.config/ReadMangaKA/"



#Uninstall

Simply remove the application launcher '~/.local/share/applications/readmanga.desktop' and clear the directory '~/.config/ReadMangaKA/src/'. If you want to remove all configuration files also, then simply delete directory '~/.config/ReadMangaKA/'. Once you delete the configuration directory, all the settings will be lost.

#Troubleshooting

If Application Launcher in the menu is not working or programme is crashing then directly go to "~/.config/ReadMangaKA/src/", open terminal there and run "python3 mangaKA.py" or "python mangaKA.py" as per your default python setup. If there is some problem in installation, then you will get idea about it, whether it is missing dependency or something else, or you can report the error as per the message in terminal.

If you do not find application launcher in the menu then try copying manually "~/.config/ReadMangaKA/readmanga.desktop" to either "~/.local/share/applications/" or "/usr/share/applications/"

In LXDE, XFCE or Cinnamon ,any new entry of launcher in '~/.local/share/applications/' is instantly shown in Start Menu (In this case, entry will be shown either in Multimedia or Sound & Video). In Ubuntu Unity you will have to either logout and login again or reboot to see the entry in Unity dash Menu.





#Brief Documentation

First select 'Source' site. Then select either Search or History sub-option. If 'Search' sub-option is selected then search-text box will appear, in which you will have to enter search keyword (Default Behaviour). If 'History' sub-option is selected, then list of Manga that you have accessed from particular  source will appear in the list below. In 'Chapters' and 'Page' Tab of the side-bar, corresponding chapter number and page number will appear for particular manga.

#KeyBoard Shortcuts:


f :  toggle fullscreen mode {In fullscreen mode mouse pointer hides automatically and can become visible for few seconds by pressing the key 'i'}

w:  fit to width

o :  original size

'=': increase size of image by 0.1 factor

'-' : decrease size of image by 0.1 factor

p:   show/hide side bar or option bar

'Down' : Simply scroll down and auto-load next page once current page reaches it's end.

'Right' : load next page (Normally no need to use it, if you are using down key. But sometimes it is useful when 'Down' key does not lead to next page)

'i' : show mouse pointer in fullscreen mode for few seconds { useful in fullscreen mode to reload image by clicking it, when mouse pointer is hidden}

Delete : Delete appropriate entry in the history/search column

If incomplete image gets loaded then simply click on the image to reload it again.

#Note: 

1. Once a page is ended, By simply pressing 'Down' key, next page is loaded automatically. It means new page is created on the fly dynamically. It does not remove previous pages and all the visited pages are kept in memory for later reference, which one can access via 'Up' or 'Down' key. Therefore, it is possible that if you've accessed large number of pages in one single session, then RAM of your system might get full, if your system has less memory. In order to free up the memory double click on the required 'chapter' of the 'Chapters' Tab of Option/Side-bar. When you select new manga then memory occupied by earlier manga is freed automatically. Alternatively, you can simply close the application to free up the memory.
 
2. In this application '/tmp/ReadManga/' acts as cache folder. If images are not loading or search function is not working then try removing contents of cache folder or simply delete the cache folder manually itself and restart the application.
