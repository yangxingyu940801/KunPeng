#!/usr/bin/env bash
#----------------------------------------------------------------------
# File       : xxx.sh
# Author     : chenzhou@china.org
# Copyright  : China Tech Pte Ltd
# Description: TODO
# Created    : Sun 09 Jul 2017 04:33:37 PM CST
# Revision   : none
#----------------------------------------------------------------------
cwd=${PWD}
if [ $# -gt 0 ]; then
  date=$1
else
  date=`date +%Y%m%d`
fi

cd 0_signal ; bash signal.sh  ${date} ; cd ${cwd}
cd 1_target ; bash target.sh  ${date} ; cd ${cwd}
cd 2_newopen; bash newopen.sh ${date} ; cd ${cwd}
cd 3_adjust ; bash adjust.sh  ${date} ; cd ${cwd}
cd 4_check  ; bash check.sh   ${date} ; cd ${cwd}

##########################################################################

# rsync data to samba server  #
########################### HY ##############################
host="chenz@192.168.2.180:/samba/0_Long_Prod"
rsync -avm 0_signal/top250/datafold/${date}/optfile     ${host}/monitor/top250/${date}.csv
rsync -avm 0_signal/mid500/datafold/${date}/optfile     ${host}/monitor/mid500/${date}.csv
rsync -avm 0_signal/botfree/datafold/${date}.csv        ${host}/monitor/botfree/${date}.csv
# rsync -avm 2_newopen/top250/datafold/*_open_${date}.*  ${host}/open/top250/
# rsync -avm 2_newopen/mid500/datafold/*_open_${date}.*  ${host}/open/mid500/
# rsync -avm 2_newopen/botfree/datafold/*_open_${date}.* ${host}/open/botfree/
for prod in hy1 hy2 hy3 hy5 hy7 zx2 xc3 rzy1; do
  rsync -avm 2_newopen/${prod}/datafold/*_${prod}open_${date}.*       ${host}/open/${prod}/
  rsync -avm  3_adjust/${prod}/datafold/${prod}_adj[b,s]*_${date}.*   ${host}/adjust/${prod}/
  rsync -avm   4_check/${prod}/datafold/${prod}_check_${date}.csv     ${host}/adjust/${prod}/
done
