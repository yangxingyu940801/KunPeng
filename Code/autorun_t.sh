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



cd 3_adjust/hywj1/datafold/
FILE_NAME=hywj1_adjust_${date}.t0.csv
echo $FILE_NAME
echo " "|mail -s "T0_Basket" -a $FILE_NAME  wujing@foreseefund.com data@qianyuanzishi.com 1048224946@qq.com


