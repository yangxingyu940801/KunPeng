#!/usr/bin/env bash
#----------------------------------------------------------------------
# File       : newopen.sh
# Author     : chenzhou@goldmine
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Tue 28 Feb 2017 10:23:53 AM CST
# Revision   : none
#----------------------------------------------------------------------
source ${HOME}/.bashrc
cwd=${PWD}
date=$1
cd top250;  python newopen.py ${date} ; cd ${cwd}
cd mid500;  python newopen.py ${date} ; cd ${cwd}
cd botfree; python newopen.py ${date} ; cd ${cwd}

cd ry1;   python newopen.py ${date} ; cd ${cwd}
cd ry3;   python newopen.py ${date} ; cd ${cwd}
cd hy1;   python newopen.py ${date} ; cd ${cwd}
cd hy2;   python newopen.py ${date} ; cd ${cwd}
cd hy3;   python newopen.py ${date} ; cd ${cwd}
cd hy5;   python newopen.py ${date} ; cd ${cwd}
#cd hy6;   python newopen.py ${date} ; cd ${cwd}
cd hy7;   python newopen.py ${date} ; cd ${cwd}
#cd hy9;   python newopen.py ${date} ; cd ${cwd}
cd hy10;  python newopen.py ${date} ; cd ${cwd}
cd rzy1;  python newopen.py ${date} ; cd ${cwd}
cd hywj1; python newopen.py ${date} ; cd ${cwd}
cd hyjq1; python newopen.py ${date} ; cd ${cwd}
cd hyjq1_pa; python newopen.py ${date} ; cd ${cwd}
cd byjx1; python newopen.py ${date} ; cd ${cwd}
cd byjx1_zt; python newopen.py ${date} ; cd ${cwd}
cd byjx2; python newopen.py ${date} ; cd ${cwd}
cd byjx3; python newopen.py ${date} ; cd ${cwd}
cd rzy1_ggt;   python newopen.py ${date} ; cd ${cwd}
cd industry_trend; python newopen.py ${date} ; cd ${cwd}
cd industry_trend_zx1; python newopen.py ${date} ; cd ${cwd}
cd zw1;  python newopen.py ${date} ; cd ${cwd}
cd zw2;  python newopen.py ${date} ; cd ${cwd}
cd zw3;  python newopen.py ${date} ; cd ${cwd}
