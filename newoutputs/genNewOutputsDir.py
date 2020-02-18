#-*- coding:utf-8 -*-
# chaonin 02.17.2020
#下面是用python代码在newoutputs目录生成v1,v2...v32共32个目录
import os
import shutil
dir = os.getcwd()
# only do version 1 now, too large, chaonin 02.18.2020
#for index1 in range(1, 33):
for index1 in range(1, 2):
	if index1 > 0:
		new_dir = dir + '/v'+ str(index1)
		os.mkdir(new_dir)
pass
