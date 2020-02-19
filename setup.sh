lua ./genScr4AllV.lua
lua ./genScr4Orig.lua
python genSpectDir.py
cd newoutputs && python genNewOutputsDir.py
cd ../versions.alt/versions.orig/ && python genTraceD.py
cd ../../source.alt/source.orig/ && make # 1st make for orig version
