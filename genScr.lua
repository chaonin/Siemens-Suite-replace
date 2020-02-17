-- CHAONIN 02.16.2020: for generating running script for all versions of replace.c --
SUITE_NAME = "replace"
CASE_NAME = 5542
VERSION_NUM = 32

--VARS--
buff = {}
i = 0
j = 0
k = 0
line_num = 0
tmp = ""


--READ ORIG SCRIPTS--
file = io.open("./scripts/runall.sh", "r")
for line in file:lines() do 
	i = i + 1;
	buff[i] = line
end 
line_num = i 
file:close()

--GENERATE RUN SCRIPT FOR VERSIONS--
for i = 1, VERSION_NUM do
k = 1
	file = io.open("./scripts/run_v"..i..".sh", "w")
	for j = 1, line_num do
		tmp = buff[j]
		if string.find(tmp, "/source.alt/source.orig/") ~=nil then
			tmp = string.gsub(tmp,"/source.alt/source.orig/", "/versions.alt/versions.orig/v"..i.."/") --modefy paths--
			tmp = string.gsub(tmp,"/outputs/", "/newoutputs/v"..i.."/")
			tmp = tmp.."\nmv trace.txt  ../versions.alt/versions.orig/v"..i
			tmp = tmp.."\ncd ../versions.alt/versions.orig/v"..i.." && pvtrace replace.exe"
			tmp = tmp.."\nmv trace.txt ./tra"..k.. " && mv graph.dot ./tra"..k
			tmp = tmp.."\ncd ../../../scripts"	
			k = k + 1
		end
		file:write(tmp.."\n")
		tmp = ""
	end
	file:close()
end
