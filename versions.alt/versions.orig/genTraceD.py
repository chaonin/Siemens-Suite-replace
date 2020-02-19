#-*- coding:utf-8 -*-
# chaonin 02.16.2020
#下面是用python代码在每个错误版本程序文件夹下生成5542个存放dot和txt的文件夹
#make_dir.py
import os
import shutil
dir = os.getcwd()
# for test, only generate for version 1, too large for all testing, 02.18.2020
#for index1 in range(1, 2):
for index1 in range(1, 33):
	if index1 > 0:
		new_dir = dir + '/v'+ str(index1)
		for index2 in range(5543):
			if index2 > 0:
				os.mkdir(new_dir + '/tra' + str(index2))
pass
