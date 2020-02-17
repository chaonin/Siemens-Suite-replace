lua ./genScr.lua
cd newoutputs && python genNewOutputsDir.py
cd ../versions.alt/versions.orig/ && python genTraceD.py
make
