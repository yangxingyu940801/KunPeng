#!/usr/bin/env bash

cwd=${PWD}
if [ $# -gt 0 ]; then
  date=$1
else
  date=`date +%Y%m%d`
fi


cd 1_target ; bash target.sh  ${date} ; cd ${cwd}
cd 2_newopen; bash newopen.sh ${date} ; cd ${cwd}
cd 3_adjust ; bash adjust.sh  ${date} ; cd ${cwd}
cd 4_check  ; bash check.sh   ${date} ; cd ${cwd}

# rsync data to samba server  #
########################### HY ##############################
host="chenz@192.168.2.180:/samba/0_Long_Prod"

#rsync -avm 2_newopen/botfree/datafold/*_open_${date}.*  ${host}/open/botfree/
for prod in ry1 ry3 hy1 hy2 hy3 hy5 hy7 hy10  rzy1 hywj1 hyjq1 hyjq1_pa industry_trend byjx1 byjx1_zt byjx2 byjx3 rzy1_ggt industry_trend_zx1 zw1 zw2 zw3; do
  rsync -avm 3_adjust/${prod}/datafold/${prod}_adj[b,s]*_${date}.*              ${host}/adjust/${prod}/
  rsync -avm 3_adjust/${prod}/datafold/${prod}_adjust_${date}.*              ${host}/adjust/${prod}/
  rsync -avm 4_check/${prod}/datafold/${prod}_check_${date}.csv                 ${host}/adjust/${prod}/
done


#FTILE_NAME=3_adjust/byjx1_zt/datafold/byjx1_zt_adjust_${date}.t0.csv
cd 3_adjust/byjx1_zt/datafold/
FILE_NAME=byjx1_zt_adjust_${date}.t0.csv
echo $FTILE_NAME
ftp  -n 47.107.126.110 << EOF
user web web\$123
passive
put $FILE_NAME
bye
EOF

echo $FILE_NAME1
echo "" | mail -s "T0_Basket" -a $FILE_NAME1  data@qianyuanzishi.com 1048224946@qq.com wujing@foreseefund.com

