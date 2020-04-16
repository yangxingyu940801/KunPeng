#!/usr/bin/env bash
#----------------------------------------------------------------------
# File       : target.sh
# Author     : chenzhou@goldmine
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Tue 28 Feb 2017 09:26:56 AM CST
# Revision   : none
#----------------------------------------------------------------------
source $HOME/.bashrc
cwd=${PWD}
date=$1
python   config.py

#cd top250;  python target.py ${date} ; cd ${cwd}
#cd mid500;  python target.py ${date} ; cd ${cwd}
#cd botfree; python target.py ${date} ; cd ${cwd}

cd ry1;   python target.py ${date} ; cd ${cwd}
cd ry3;   python target.py ${date} ; cd ${cwd}
cd hy1;   python target.py ${date} ; cd ${cwd}
cd hy2;   python target.py ${date} ; cd ${cwd}
cd hy3;   python target.py ${date} ; cd ${cwd}
cd hy5;   python target.py ${date} ; cd ${cwd}
#cd hy6;   python target.py ${date} ; cd ${cwd}
cd hy7;   python target.py ${date} ; cd ${cwd}
#cd hy9;   python target.py ${date} ; cd ${cwd}
cd hy10;  python target.py ${date} ; cd ${cwd}
cd rzy1;  python target.py ${date} ; cd ${cwd}
cd hywj1; python target.py ${date} ; cd ${cwd}
cd hyjq1; python target.py ${date} ; cd ${cwd}
cd hyjq1_pa; python target.py ${date} ; cd ${cwd}
cd byjx1; python target.py ${date} ; cd ${cwd}
cd byjx1_zt; python target.py ${date} ; cd ${cwd}
cd byjx2; python target.py ${date} ; cd ${cwd}
cd byjx3; python target.py ${date} ; cd ${cwd}
cd rzy1_ggt;   python target.py ${date} ; cd ${cwd}
cd industry_trend; python target.py ${date} ; cd ${cwd}
cd industry_trend_zx1; python target.py ${date} ; cd ${cwd}
cd zw1; python target.py ${date} ; cd ${cwd}
cd zw2; python target.py ${date} ; cd ${cwd}
cd zw3; python target.py ${date} ; cd ${cwd}
