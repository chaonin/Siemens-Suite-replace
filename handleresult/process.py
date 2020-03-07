#-*- coding:utf-8 -*-
# chaonin 02.24.2020
import datetime
import re
import math

VER = 32					# versions number
TEST = 5542					# test cases number
LINE = 600 					# original version's line is 565, all bug versions may exceed 565, currently given 600! 
ACTUALLINE = [0]*VER 		# actual line of all versions
RESULT = []					# running result of all versions
for i in range(VER):
	RESULT.append([1]*TEST) # the default value is 1 - PASS
ef = []						# the failed results that executed this line code
ep = []						# the passed results that executed this line code
nf = []						# the failed results that not executed this line code
np = []						# the passed results that not executed this line code
for i in range(VER):
	ef.append([0]*LINE)
	ep.append([0]*LINE)
	nf.append([0]*LINE)
	np.append([0]*LINE)
Jaccard = [0]*LINE			# Jaccard result 
SUSLINE_J = [0]*VER			# the suspecious line for bug of Jaccard
SUSLINE_O = [0]*VER			# the suspecious line for bug of Ochiai
SUSLINE_T = [0]*VER			# the suspecious line for bug of Tarantula 
SUSLINE_D1 = [0]*VER		# the suspecious line for bug of D1
SUSLINE_D2 = [0]*VER		# the suspecious line for bug of D2
SUSLINE_D3 = [0]*VER		# the suspecious line for bug of D3 
SUSLINE_EP2 = [0]*VER		# the suspecious line for bug of EP2
SUSLINE_EP3 = [0]*VER		# the suspecious line for bug of EP3 

SPECTMATRIX = []
for i in range(LINE):
	SPECTMATRIX.append([0]*TEST)
#end for

#fetch output result of all versions
for v in range(1,VER+1):
	if(v == 27):# version 27 gcov info missing
		continue

	fn = "../finalresults/diff_output_vo_v" + str(v)
	fr = open(fn,'r')
	content = fr.read()
	lines = content.split('\n')		
	lineno = len(lines) 
	for l in range(0,lineno-1):
		mo = re.match('.*outputs.*?(\d*) and newoutputs.*', lines[l])
		if (mo):
			RESULT[v-1][int(mo.group(1))-1] = 0 # FAIL
	#end for
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print time, "all running result processing ok"

# fetch the spectrum info of all versions
for v in range(1,VER+1):
	if(v == 27 ):# version 27 gcov info missing
		continue
	if(v == 32 ):# ep + ef + nf = 0, divide by 0 for Jarccard! --- Bug of statistics of None executable line ?
		continue

	for t in range(1,TEST+1):
		fname = "../spectrum/V" + str(v) + "/t" + str(t) + "/replace.c.gcov"
		fhandle = open(fname, "r")
		content = fhandle.read()
		
		lines = content.split('\n')		
		lineno = len(lines) 
		linecnt = 0
		for i in range(5, lineno-1):
			linecnt = linecnt + 1
			if (re.match('^.*\d+:  *\d*:.*', lines[i])): # Have been executived
				SPECTMATRIX[i-5][t-1] = 1	
			#elif (re.match('^.*#####:.*', lines[i])):	# Have not been executived (default is 0, not been executived.
			#	SPECTMATRIX[i-5][t-1] = 0
			elif (re.match('^.*-:  *\d*:.*', lines[i])):	# Not executable line, such as definition line
				SPECTMATRIX[i-5][t-1] = -1
		#end for i		
	#end for t
	ACTUALLINE[v-1] = linecnt
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print time, "spectrum matrix processing ok for v%d" % v

	for j in range(0, ACTUALLINE[v-1]):
		for k in range(0, TEST):
			if  (SPECTMATRIX[j][k] == 1 and RESULT[v-1][k] == 1):
				ep[v-1][j] += 1
			elif(SPECTMATRIX[j][k] == 1 and RESULT[v-1][k] == 0):
				ef[v-1][j] += 1
			elif(SPECTMATRIX[j][k] == 0 and RESULT[v-1][k] == 1):
				np[v-1][j] += 1
			elif(SPECTMATRIX[j][k] == 0 and RESULT[v-1][k] == 0):
				nf[v-1][j] += 1
	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print time, "ep ef np nf processing ok for v%d" % v
	
	############################ begin of different metrics #############################
	print "              EP    EF   NP    NF Jaccard Ochiai Tarantula   D1   D2   D3    EP2    EP3"
	susmax_J = 0
	susmax_O = 0
	susmax_T = 0
	susmax_D1 = 0
	susmax_D2 = 0
	susmax_D3 = 0
	susmax_EP2 = 0
	susmax_EP3 = 0
	for line in range(0, ACTUALLINE[v-1]):
		if (SPECTMATRIX[line][0] == -1): # any test for this code line is not been executable(here we use version 1), such as definition line
			continue					 # need not metric for this line
		Jaccard = float(ef[v-1][line])/(ef[v-1][line] + nf[v-1][line] + ep[v-1][line])	 # will (ef[v-1][line] + nf[v-1][line] + ep[v-1][line]) be zero? currently not found, shoud be shown!
		if ( (ef[v-1][line]+nf[v-1][line]) == 0 or (ef[v-1][line]+ep[v-1][line]) == 0 ): # not to measure this line, will cause divide by 0 !!!
			continue
		Ochiai = float(ef[v-1][line])/math.sqrt((ef[v-1][line]+nf[v-1][line])*(ef[v-1][line]+ep[v-1][line]))
		#if(ef[v-1][line] + nf[v-1][line] == 0 or ep[v-1][line]+np[v-1][line] == 0 or ef[v-1][line]+nf[v-1][line] == 0 ):
		#	continue
		Tarantula = float(ef[v-1][line])/(ef[v-1][line] + nf[v-1][line]) / ((float(ep[v-1][line])/(ep[v-1][line]+np[v-1][line])) + (float(ef[v-1][line])/(ef[v-1][line]+nf[v-1][line])))
		D1 = float(ef[v-1][line])/(nf[v-1][line] + ep[v-1][line])
		D2 = 2*float(ef[v-1][line])/(nf[v-1][line] + ep[v-1][line])
		D3 = 3*float(ef[v-1][line])/(nf[v-1][line] + ep[v-1][line])
		EP2 = float(ef[v-1][line])/(nf[v-1][line] + pow(ep[v-1][line], 1/2.0))
		EP3 = float(ef[v-1][line])/(nf[v-1][line] + pow(ep[v-1][line], 1/3.0))
		if (Jaccard > susmax_J):
			susmax_J = Jaccard
			SUSLINE_J[v-1] = line + 1
		if (Ochiai > susmax_O):
			susmax_O = Ochiai 
			SUSLINE_O[v-1] = line + 1
		if (Tarantula > susmax_T):
			susmax_T = Tarantula
			SUSLINE_T[v-1] = line + 1
		if (D1 > susmax_D1):
			susmax_D1 = D1
			SUSLINE_D1[v-1] = line + 1
		if (D2 > susmax_D2):
			susmax_D2 = D2
			SUSLINE_D2[v-1] = line + 1
		if (D3 > susmax_D3):
			susmax_D3 = D3
			SUSLINE_D3[v-1] = line + 1
		if (EP2 > susmax_EP2):
			susmax_EP2 = EP2
			SUSLINE_EP2[v-1] = line + 1
		if (EP3 > susmax_EP3):
			susmax_EP3 = EP3
			SUSLINE_EP3[v-1] = line + 1
		print 'line %3d: %5d %5d %5d %5d  %.3f  %.3f  %.7f %.3f %.3f %.3f %.3f %.3f' % (line+1, ep[v-1][line], ef[v-1][line], np[v-1][line], nf[v-1][line], Jaccard, Ochiai, Tarantula, D1, D2, D3, EP2, EP3)

	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print time, "metrics processing ok for v%d" % v
	#print susmaxline_J+1, susmaxline_O+1
	#print susmax_J, susmax_O
	
#end for v

for v in range(1,VER+1):
	print "v%2d: %4d %4d %4d %4d %4d %4d %4d %4d" % (v, SUSLINE_J[v-1], SUSLINE_O[v-1], SUSLINE_T[v-1], SUSLINE_D1[v-1], SUSLINE_D2[v-1], SUSLINE_D3[v-1], SUSLINE_EP2[v-1], SUSLINE_EP3[v-1])
