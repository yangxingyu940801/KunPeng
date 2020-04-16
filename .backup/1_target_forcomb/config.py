#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# File       : config.py
# Author     : chenzhou@china.org
# Copyright  : China Tech Pte Ltd
# Description: TODO
# Created    : Wed 12 Jul 2017 03:37:51 PM CST
# Revision   : none
#----------------------------------------------------------------------
import os
import sys
import logbook
import numpy as np
import pandas as pd
from commbase.commbase import CommBase


class Config(CommBase):
    def __init__(self):
        super(Config, self).__init__()
        self.logger = logbook.Logger('[Config]')
        self.config = "/samba/0_Long_Prod/config/%N.xlsm"

        self.stgpath = {}
        self.stgpath['jg']    = '/home/chenz/production/longonly/0_signal/others/JG/datafold/jungong.csv'
        self.stgpath['xlc']    = '/home/chenz/production/longonly/0_signal/others/XLC/datafold/lanchou.csv'
        self.stgpath['gf']    = '/home/chenz/production/longonly/0_signal/others/GF/datafold/gfmodel.csv'
        self.stgpath['wlw']   = '/home/chenz/production/longonly/0_signal/others/WLW/datafold/wlwmodel.csv'
        self.stgpath['yjs']   = '/home/chenz/production/longonly/0_signal/others/YJS/datafold/yjsmodel.csv'
        self.stgpath['gyhlw'] = '/home/chenz/production/longonly/0_signal/others/GYHLW/datafold/gyhlwmodel.csv'
        self.stgpath['AI'] = '/home/chenz/production/longonly/0_signal/others/AI/datafold/aimodel.csv'
        self.stgpath['CX'] = '/home/chenz/production/longonly/0_signal/others/CX/datafold/cxmodel.csv'
        self.stgpath['lc'] = '/home/chenz/production/longonly/0_signal/others/LC/datafold/lcmodel.csv'
        self.stgpath['xa'] = '/home/chenz/production/longonly/0_signal/others/XA/datafold/xamodel.csv'
        self.stgpath['hd'] = '/home/chenz/production/longonly/0_signal/others/HD/datafold/hdmodel.csv'
        self.stgpath['bdt'] = '/home/chenz/production/longonly/0_signal/others/BDT/datafold/bdtmodel.csv'
        self.stgpath['xny'] = '/home/chenz/production/longonly/0_signal/others/XNY/datafold/xnymodel.csv'
        self.stgpath['5G'] = '/home/chenz/production/longonly/0_signal/others/5G/datafold/5g.csv'
        self.stgpath['xxf'] = '/home/chenz/production/longonly/0_signal/others/XXF/datafold/xxfmodel.csv'
        self.stgpath['szzg'] = '/home/chenz/production/longonly/0_signal/others/SZZG/datafold/szzgmodel.csv'
        self.stgpath['gdgs'] = '/home/chenz/production/longonly/0_signal/others/GDGS/datafold/gdgsmodel.csv'
        self.stgpath['ppp'] = '/home/chenz/production/longonly/0_signal/others/PPP/datafold/pppmodel.csv'
        self.stgpath['cxyy'] = '/home/chenz/production/longonly/0_signal/others/CXYY/datafold/cxyymodel.csv'
        self.stgpath['cddg'] = '/home/chenz/production/longonly/0_signal/others/CDDG/datafold/cddgmodel.csv'
        self.stgpath['cyhlw'] = '/home/chenz/production/longonly/0_signal/others/CYHLW/datafold/cyhlwmodel.csv'
        self.stgpath['gjd'] = '/home/chenz/production/longonly/0_signal/others/GJD/datafold/gjdmodel.csv'
        self.stgpath['djl'] = '/home/chenz/production/longonly/0_signal/others/DJL/datafold/djlmodel.csv'
        self.stgpath['xitu'] = '/home/chenz/production/longonly/0_signal/others/XITU/datafold/xitu.csv'
        self.stgpath['apple'] = '/home/chenz/production/longonly/0_signal/others/APPLE/datafold/apple.csv'
        self.stgpath['wlaq'] = '/home/chenz/production/longonly/0_signal/others/WLAQ/datafold/wlaq.csv'
        self.stgpath['ggx'] = '/home/chenz/production/longonly/0_signal/others/GAOGUXI/datafold/ggx.csv'
        self.stgpath['hkfl'] = '/home/chenz/production/longonly/0_signal/others/HKFL/datafold/%Y%m%d.csv'
        self.stgpath['keji'] = '/home/chenz/production/longonly/0_signal/others/KEJI/datafold/kjmodel.csv'
        self.stgpath['kechuangban'] = '/home/chenz/production/longonly/0_signal/others/KECHUANGBAN/datafold/kcbmodel.csv'
        self.stgpath['ZQ_ZZ1000_HTVR'] = '/13data/EnhancedIndex/ZZ1000_highTVR/$date/optfile'
        self.stgpath['ZQ_ZZ1000'] = '/13data/EnhancedIndex/ZZ1000/$date/optfile'
        self.stgpath['ZQ_HS300'] = '/13data/EnhancedIndex/HS300/$date/optfile'
        self.stgpath['ZQ_CYB'] = '/13data/EnhancedIndex/CYB/$date/optfile'
        self.stgpath['ZQ_ZZ500'] = '/13data/EnhancedIndex/ZZ500/$date/optfile'
        self.stgpath['ZQ_ZZ500_SH'] = '/13data/EnhancedIndex/ZZ500_SH/$date/optfile'
        self.stgpath['ZQ_ZZ500_HTVR'] = '/13data/EnhancedIndex/ZZ500_highTVR/$date/optfile'
        self.stgpath['ZQ_MSCI'] = '/13data/EnhancedIndex/MSCI/$date/optfile'

    def work(self, date):
        config = [] 
        for name in ['zyc','dy', 'xp', 'szj']:
            fn = self.config.replace("%N", name)
            xl = pd.ExcelFile(fn)
            df = xl.parse('sheet') * 100
            config.append(df)
        config = pd.concat(config)

        for prod, ratio in config.iterrows():
            confile = prod + "/config"
            with open(confile, "w") as fout:
                fout.write("[input]\n")
                fout.write("limit=0.0001\n")
                for model in config.columns:
                    weight = ratio[model]
		    if model=='manual': continue
                    if np.isnan(weight): continue
                    if weight < 0.00001: continue
                    if model not in self.stgpath: raise Exception('invalid model %s in %s' %(model, prod))
                    fout.write("\n")
                    fout.write("weight_%s=%.3f\n" %(model, weight))
                    fout.write("signal_%s=%s\n"   %(model, self.stgpath[model]))
                fout.write("\n")
                fout.write("[output]\n")
                fout.write("outfile=datafold/%Y%m%d.csv")
            self.logger.info("suceed updating config file for {}", prod)


if __name__ == "__main__":
    job = Config()
    job.run()
