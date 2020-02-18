cd ./scripts && rm -rf run_v*
cd ../outputs && rm -rf t* #rm all outputs of replace from original version
cd ../newoutputs && rm -rf v* #rm all outputs of all versions
cd ../ && rm -rf spectrum/ # rm all spectrum related info 
cd versions.alt/versions.orig/v1/ && rm -rf tra* # rm all output of dir "tra" (for pvtrace), current just do version 1
