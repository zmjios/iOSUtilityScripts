#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 

__author__ = "zmjios"
__date__ = "2016-08-03"

import os
import os.path
import re
import sys

#检测.a 或者mach-o文件是否是fat文件
def verified_macho_path(path):
	if not os.path.isfile(path):
		return None

	## Apparently there is a bug in otool -- it doesn't seem to like executables
	## with spaces in the names. If this is the case, make a copy and analyze that.
	if ' ' in os.path.basename(path):
		## don't remove the spaces, that could lead to an empty string
		new_filename = path.replace(' ', '_')
		new_path = os.path.join(tempfile.mkdtemp(), new_filename)
		shutil.copy(path, new_path)
		path = new_path

	cmd = "/usr/bin/file -b %r" % path
	cmd2 = "lipo -info %s | grep architecture:" % path
	s = os.popen(cmd).read()
	s2 = os.popen(cmd).read()

	if not s.startswith('Mach-O') or len(s2.strip()) < 1:
		return None

	return path


#分离对应的fat文件
def checkFatFile(args):
	path = sys.argv[1]
	arch_list = []
	unusedclasslist = []
	classlist = []
	classrefs = []
	lines = os.popen("lipo -detailed_info %s" % path).readlines()
	for line in lines:
		if line.startswith("architecture"):
			arch_list.append(line[10:]).strip()
	#分离对应的mach-o文件，找出其中未使用的类名
	for arch in arch_list:
		os.makedirs("temp/%s" % arch)
		currentpath = "temp/%s" % path + "_" + arch + ".a"
		os.popen("lipo %s -thin %s -output %s" % (path,arch,currentpath))

	tempPath = os.getcwd() + "/temp"
	#分离出目标文件(.o)
	for root,subdirs,files in os.walk(tempPath):
		for subfile in files:
			if subfile.endswith(".a"):
				if verified_macho_path(subfile) != None:
					os.popen("ar -x %s" % subfile)		
	#找出未使用的.o文件，遍历一个即可，因为不同的架构代码都一样
	for root,subdirs,files in os.walk(tempPath):
		for subfile in files:
			if subfile.endswith(".a"):
				mach_o = subfile
				mlines = os.popen("otool -V -s __DATA __objc_classlist %s | grep %s" % (mach_o,mach_o)).readlines()
				for line in mlines:
					if lines.startswith(mach_o):
						classlist.append(line[len(mach_o):len(line)-2])
					mlines = os.popen("otool -V -s __DATA __objc_classrefs %s | grep %s" % (mach_o,mach_o)).readlines()
				for line in mlines:
					if lines.startswith(mach_o):
					classrefs.append(line[len(mach_o):len(line)-2])
			break

	for subfile in classlist:
		if subfile not in classrefs:
			print("*********** %s 没有使用 *********" % subfile)
			unusedclasslist.append(subfile)

	#添加过滤条件，有些代码调用通过总线或者nsstringfrom或者performSelector调用

	#遍历不同架构的目录，删除未使用.o文件
	
		



	


if __name__ == "__main__":

	path = verified_macho_path(sys.argv)
	if not path:
		print "Usage: %s MACH_O_FILE" % sys.argv[0]
		sys.exit(1)
	checkFatFile(sys.argv)
