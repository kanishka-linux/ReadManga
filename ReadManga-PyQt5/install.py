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

import os
from os.path import expanduser
import shutil
import subprocess
import platform
home1 = expanduser("~")
#home1 = "/usr/local/share"
home = home1+"/.config/ReadMangaKA"
nHome = home+'/src' 

if not os.path.exists(home):
	os.makedirs(home)

if os.path.exists(nHome):
	n = os.listdir(nHome)
	for i in n:
		k = nHome+'/'+i
		if os.path.isfile(k):
			os.remove(k)

if not os.path.exists(nHome):
	os.makedirs(nHome)
cwd = os.getcwd()
m = os.listdir(cwd)
for i in m:
	k = cwd+'/'+i
	shutil.copy(k,nHome)

f = open('readmanga.desktop','r')
lines = f.readlines()
f.close()
os_name = platform.platform()

os_name = os_name.lower()
print(os_name)
if 'arch' in os_name:
	lines[5]="Exec=python "+nHome+'/mangaKA.py'+'\n'
else:
	lines[5]="Exec=python3 "+nHome+'/mangaKA.py'+'\n'
f = open(home+'/readmanga.desktop','w')
for i in lines:
	f.write(i)
f.close()

#picn = home+'/default.jpg'
#if not os.path.exists(picn):
#	shutil.copy('default.jpg',home+'/default.jpg')
	
dest_file = home1+'/.local/share/applications/readmanga.desktop'

#subprocess.call(['sudo','cp',home+'/readmanga.desktop',dest_file])
shutil.copy(home+'/readmanga.desktop',dest_file)

print("Application Launcher: "+dest_file)
print ("\nInstalled Successfully!\n")
