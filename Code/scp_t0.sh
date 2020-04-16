date=$1
cd /home/jiangtz/TestExec/3_adjust/byjx1_zt/datafold/
FILE_NAME=byjx1_zt_adjust_${date}.t0.csv
echo $FTILE_NAME
ftp -n 47.107.126.110 << EOF
user web web\$123
passive
put $FILE_NAME
bye
EOF
