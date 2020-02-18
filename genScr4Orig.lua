-- CHAONIN 02.16.2020: for generating running script for all versions of replace.c --
SUITE_NAME = "replace"
CASE_NAME = 5542
VERSION_NUM = 32

--VARS--
buff = {}
i = 0
j = 1
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

--GENERATE NEW RUN SCRIPT FOR ORIG VERSION--
file = io.open("./scripts/runall_new.sh", "w")
for i = 1, line_num do
	tmp = buff[i]
	if string.find(tmp, "/source.alt/source.orig/") ~=nil then
		tmp = tmp.."\ncd ../source.alt/source.orig/ && gcov replace.c "
		tmp = tmp.."\nmv ./replace.c.gcov ../../spectrum/Vo/t"..j.."/"
		tmp = tmp.."\nmake"	
		tmp = tmp.."\ncd ../../scripts"	
		j = j + 1
	end
	file:write(tmp.."\n")
	tmp = ""
end
file:close()
