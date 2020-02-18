#-*- coding:utf-8 -*-
# chaonin 02.18.2020
# make spectrum dir for orig and all versions repace.c   
#make_dir.py
import os
import shutil

dir = os.getcwd()
new_dir = dir + '/spectrum' # make a spectrum dir in top dir 
os.mkdir(new_dir)

#make sub dir for all versions
new_dir = new_dir + '/Vo'
os.mkdir(new_dir)


#make sub dir for all test
for index1 in range(5543):
	if index1 > 0:
		os.mkdir(dir + '/spectrum/Vo/t' + str(index1))
for index1 in range(1, 33):
	if index1 > 0:
		new_dir = dir + '/spectrum/V'+ str(index1)
		os.mkdir(new_dir)
		for index2 in range(5543):
			if index2 > 0:
				os.mkdir(new_dir + '/t' + str(index2))
