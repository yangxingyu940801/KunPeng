#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : __init__.py
# Author     : chenzhou@goldmine
# Copyright  : ForeSee Fund Pte Ltd
# Description: TODO
# Created    : Wed 01 Mar 2017 11:22:02 AM CST
# Revision   : none
#----------------------------------------------------------------------
import xlwt
import xlrd
import logbook
import numpy as np
import pandas as pd

def xls2df(fn):
    book = xlrd.open_workbook(fn)
    sheet = book.sheet_by_name("sheet")
    data = []
    for i in range(sheet.nrows):
        tmp = []
        for j in range(sheet.ncols):
            msg = str(sheet.cell(i, j))
            tmp.append(str(msg.strip().split(":")[1]))
        data.append(tmp)
    df = pd.DataFrame(data[1:])
    df.columns = data[0]
    return df


def df2xls(fn, df, header=True):
    nrow, ncol = df.shape
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet')
    
    if header:
        for j in range(ncol):
            sheet.write(0, j, df.columns[j])
        for i in range(nrow):
            for j in range(ncol):
                sheet.write(i+1, j, df.ix[i, j])
    else:
        for i in range(nrow):
            for j in range(ncol):
                sheet.write(i, j, df.ix[i, j])
    book.save(fn)
