#!/usr/bin/env bash
source $HOME/.bashrc

cwd=${PWD}
date=$1

echo adjust------------

for d in $(ls -F ../3_adjust/ | grep '/$')
do
	echo ${d}
	scp ../3_adjust/$d/adjbas/*$1* liulc@192.168.2.180:/samba/moneymaker/adjust/$d/
done

