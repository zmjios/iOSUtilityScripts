#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 

__author__ = "zmjios"
__date__ = "2016-08-05"


import os
import re
import sys

all3ximgs = []
all2ximgs = []
alldeleteimgs = []
img2xsuf = "@2x.png"
img3xsuf = "@3x.png"
filterimg = "icon_xiecheng"

def deleteAll2ximg():
	for root,subdirs,files in os.walk(os.getcwd()):
		for subfile in files:
			if subfile.endswith(img2xsuf) and subfile.startswith(filterimg) == False:
				all2ximgs.append(os.path.join(root,subfile))
			if subfile.endswith(img3xsuf) and subfile.startswith(filterimg) == False:
				all3ximgs.append(os.path.join(root,subfile))
	for img3x in all3ximgs:
		img3xname = os.path.split(img3x)[1]
		for img2x in all2ximgs:
			img2xname = os.path.split(img2x)[1]
			if img2xname[0:len(img2xname) - len(img2xsuf)] == img3xname[0:len(img3xname) - len(img3xsuf)]:
				alldeleteimgs.append(img2x)

	totalsize = 0.0
	for root,subdirs,files in os.walk(os.getcwd()):
		for subfile in files:
			for deleteimg in alldeleteimgs:
				if deleteimg == os.path.join(root,subfile):
					totalsize = totalsize + os.path.getsize(deleteimg)
					print("*********正在删除图片%s*********" % deleteimg)
					#os.system("rm -rf %s" % deleteimg)
	print("**********删除图片的总大小为:%.4fKB*************" % (totalsize / 1024.0))

if __name__ == "__main__":
	deleteAll2ximg()



	