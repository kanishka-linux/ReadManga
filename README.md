#ReadManga :  A GNU/Linux Desktop Application for reading Japanese Manga from various sites available on the internet.

**Note:** This application fetches manga images from various sites available on the internet.
Therefore, before using this application please check the copyright and licensing laws of your country. Because it's possible that some of these Manga might be already licensed in your country. Therefore use this application at your own risk. Author of the 'ReadManga' application is not at all related to any of these sites or their content provider. This application is simply a desktop client that fetches manga images from sites on the internet. If the site from which this application fetches images either closes or changes it's source, then this application will also fail to perform it's designated function. 


(If You've Already installed application using common method and now want to re-install it again using either .deb and .pkg.tar.xz or you want to try PyQt5 version, then first remove readmanga.desktop file located in '~/.local/share/applications/' and also remove config directory '~/.config/ReadMangaKA/src/')

#Update ReadManga-2.1.0-1

1. 'python-requests' no longer required.

#Update ReadManga-2.0.0-1

1. 'phantomjs' no longer required. The reader has it's version of headless browser with javascript support.

2. 'wget' no longer required

3. Proper implementation of multithreading, so as to allow proper pre-fetching of next page. As a result flow of reading will not interrupt as long as next page is available at the source site and your internet connection is neither down nor slow. {If your internet connection is slow or the source site is slow then you might have to wait after end of the page for the next page to show up.}

4. Corrupt or Half downloaded pages will be reloaded automatically, if they are available at later time.

5. Right, Left arrow key for navigating previous and next page, using these keys will free up the memory consumed by previous pages. Useful for low RAM machines. You can also use these keys after long reading session in order to free up the memory and delete previously accessed pages.

#Screenshot
![ReadManga](/Images/sample.png)

#Note : 

1. ReadManga-PyQt4-Stable is Stable version (Inside ReadManga-PyQt4-Stable Directory) and written in pyqt4 and python3.

2. ReadManga-PyQt5-Experimental is experimental version (Inside ReadManga-PyQt5-Experimental Directory: Currently Working only in Arch-Linux) and written in pyqt5 and python3.

3. If you've installed the Application using .deb or PKGBUILD, and somehow application launcher in the menu is not working, then open terminal and launch the application using command 'python -B /usr/share/ReadManga/mangaKA.py' or 'python3 -B /usr/share/ReadManga/mangaKA.py'.

#Dependencies and Installation:

**Arch:** PKGBUILD is available in Arch specific folder. First create pkg using command **'makepkg -s'** and then install using **'sudo pacman -U pkg_name'** (If user want to try PyQt5 version then first rename 'PKGBUILD-PyQt5' to 'PKGBUILD' before using it.)

**Ubuntu or Debian based distro:** users can directly go to Release section,download appropriate .deb package and install it using **'sudo gdebi pkg_name.deb'**. It will resolve all the dependencies while installing the package. Normally 'dpkg -i' is used for installing .deb package in Debian based distros, but 'dpkg' won't install dependencies automatically, which users have to install manually as per instructions given below. Hence try to use 'gdebi' for convenience. For removing the package use 'sudo apt-get remove ReadManga' 

#Dependencies

python3

python-pyqt4 {for stable ReadManga Application}

python-pyqt5 (for experimental ReadManga-PyQt5 Application)

python-pillow

python-beautifulsoup4

python-lxml

python-pycurl

curl

##Dependencies installation in arch (Stable Version).

sudo pacman -S python python-pyqt4 python-pycurl python-pillow python-beautifulsoup4 python-lxml curl

##In ubuntu 14.04, default python points to python 2.7, hence for installing dependencies use following command (Stable Version)

sudo apt-get install python3 python3-pyqt4 python3-pycurl python3-pil python3-bs4 python3-lxml curl

##Dependencies installation in arch (Experimental Version i.e. ReadManga-PyQt5).

sudo pacman -S python python-pyqt5 python-pycurl python-pillow python-beautifulsoup4 python-lxml curl

In ubuntu 14.04, Experimental Version i.e. ReadManga-PyQt5 is not working 

Once Dependencies are installed Download the folder. Goto ReadManga Directory containing 'install.py' file (If you want stable version of the application written in pyqt4). If you want to try experimental version of the application written in pyqt5 then goto ReadManga-PyQt5 Directory containing 'install.py' file. 


Once you are inside the required directory, Open Terminal in the directory and execute **'python3 mangaKA.py'** to open the application directly or use following command to create application launcher:

###In Arch:

python install.py

###In Ubuntu 14.04+:

python3 install.py

Application Launcher will be created as "~/.local/share/applications/readmanga.desktop"

All other configuration files will be created in "~/.config/ReadMangaKA/"



#Uninstall

Simply remove the application launcher '~/.local/share/applications/readmanga.desktop' and clear the directory '~/.config/ReadMangaKA/src/'. If you want to remove all configuration files also, then simply delete directory '~/.config/ReadMangaKA/'. Once you delete the configuration directory, all the settings will be lost.

#Troubleshooting

If Application Launcher in the menu is not working or programme is crashing then directly go to "~/.config/ReadMangaKA/src/", open terminal there and run "python3 mangaKA.py" or "python mangaKA.py" as per your default python setup. If there is some problem in installation, then you will get idea about it, whether it is missing dependency or something else, or you can report the error as per the message in terminal.

If you do not find application launcher in the menu then try copying manually "~/.config/ReadMangaKA/readmanga.desktop" to either "~/.local/share/applications/" or "/usr/share/applications/"

In LXDE, XFCE or Cinnamon ,any new entry of launcher in '~/.local/share/applications/' is instantly shown in Start Menu (In this case, entry will be shown either in Multimedia or Sound & Video). In Ubuntu Unity you will have to either logout and login again or reboot to see the entry in Unity dash Menu.

If some source sites are not working then try clearing the cache directory '/tmp/ReadManga/' and relaunch the application.

If next page does not load smoothly, try increasing/decreasing size of image using '-/=' keys or try removing "~/.config/ReadMangaKA/config.txt" and restart the application.


#Brief Documentation

First select 'Source' site. Then select either Search or History sub-option. If 'Search' sub-option is selected then search-text box will appear, in which you will have to enter search keyword (Default Behaviour). If 'History' sub-option is selected, then list of Manga that you have accessed from particular  source will appear in the list below. In 'Chapters' and 'Page' Tab of the side-bar, corresponding chapter number and page number will appear for particular manga.

#KeyBoard Shortcuts:


f : toggle fullscreen mode {In fullscreen mode mouse pointer hides automatically and can become visible for few seconds by pressing the key 'i'}

w:  fit to width {aspect ratio as per the last visited image}

shift+w: fit to width but doesn't keep aspect ratio {pressing 'h' and then 'shift+w' will fit the image both widthwise and heightwise}

h:  fit to height {aspect ratio as per the last visited image} 

o:  gets the original aspect ratio of last visited image, and sets same aspect ratio for all image.

a:  show strictly original images with no scaling.

'=': increase size of image by 0.01 factor by keeping aspect ratio constant.

'-': decrease size of image by 0.01 factor by keeping aspect ratio constant.

p:   show/hide side bar or option bar

1: View Mode 1 (Default mode, keeps only 5 last pages in memory, consumes less memory)

2: View Mode 2 (Keeps all the pages in memory, memory consuming mode)

'Down' : Simply scroll down and auto-load next page once current page reaches it's end.

'ctrl+Right' : load next page (Normally no need to use it, if you are using down key. But sometimes it is useful when 'Down' key does not lead to next page)

'ctrl+Left' : load previous page

{using Left and Right arrow key will delete previously accessed pages and clear up the memory}

'i' : show mouse pointer in fullscreen mode for few seconds { useful in fullscreen mode to reload image by clicking it, when mouse pointer is hidden}

Delete : Delete appropriate entry in the history/search column

If incomplete image gets loaded then simply click on the image to reload it again.

#Note: 

1. Once a page is ended, By simply pressing 'Down' key, next page is loaded automatically. It means new page is created on the fly dynamically. It does not remove previous pages and all the visited pages are kept in memory for later reference, which one can access via 'Up' or 'Down' key. Therefore, it is possible that if you've accessed large number of pages in one single session, then RAM of your system might get full, if your system has less memory. In order to free up the memory double click on the required 'chapter' of the 'Chapters' Tab of Option/Side-bar or simply try using ctrl+Left/Right arrow keys. When you select new manga then memory occupied by earlier manga is freed automatically. Alternatively, you can simply close the application to free up the memory. {Now Applicable only for View Mode 2}
 
2. In this application '/tmp/ReadManga/' acts as cache folder. If images are not loading or search function is not working then try removing contents of cache folder or simply delete the cache folder manually itself and restart the application.
