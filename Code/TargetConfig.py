#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logbook
import numpy as np
import pandas as pd
import datetime
from MyDB import getAdjprc
from commbase.commbase import CommBase
import warnings
warnings.filterwarnings("ignore")

class Config(CommBase):
    def __init__(self):
        super(Config, self).__init__()
        self.logger = logbook.Logger('[Config]')
        self.configfile = "/samba/0_Long_Prod/config/%N.xlsm"
        self.path = "/home/jiangtz/TestExec/1_target"

        self.GenQFZ()
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
        self.stgpath['ZQ_ZZ500_HGT'] = '/13data/EnhancedIndex/ZZ500_hgt/$date/optfile'
        self.stgpath['ZQ_ZZ1000_HGT'] = '/13data/EnhancedIndex/ZZ1000_hgt/$date/optfile'
        self.stgpath['ZQ_HS300_HGT'] = '/13data/EnhancedIndex/HS300_hgt/$date/optfile'
        self.stgpath['ZQ_CYB_HGT'] = '/13data/EnhancedIndex/CYB_hgt/$date/optfile'
        self.stgpath['IH_QFZ'] = '/home/jiangtz/TestExec/IndexComp/IH/$date.csv'
        self.stgpath['ZQ_CYB50'] = '/home/jiangtz/TestExec/IndexComp/CYB50/$date.csv'

    def GenQFZ(self, save_dir = "/home/jiangtz/TestExec/IndexComp"):
        date = datetime.datetime.now().strftime("%Y%m%d")
        self.indexpreclose = getAdjprc(date)
        codes = ["IH", "IF", "IC", "CYB50"]
        for code in codes:
            if code=='IH':
                path='/13data/QuantData/DailyData/Index/IndexComp/csv/Comp/000016.SH'
            elif code=='IF':
                path='/13data/QuantData/DailyData/Index/IndexComp/csv/Comp/399300.SZ'
            elif code=='IC':
                path='/13data/QuantData/DailyData/Index/IndexComp/csv/Comp/000905.SH'
            elif code=='CYB50':
                path='/13data/QuantData/DailyData/Index/IndexComp/csv/Comp/399673.SZ'


            df=pd.read_csv(path,index_col=0)
            df.index=[int(str(s).replace('-','')) for s in df.index]
            dateint=int(date)
            weight=df[df.index<dateint].iloc[-1,:]
            weight=weight[weight>0]
            tempPath = os.path.join(save_dir, code)
            if not os.path.exists(tempPath):
                os.makedirs(tempPath)
            weight.to_csv(os.path.join(tempPath, str(date)+'.csv'),sep='|')

    def GetHedgeRatio(self):
        temp = pd.read_excel("/samba/moneymaker/Strategy.xlsx")
        temp.columns = range(len(temp.columns))
        temp = temp[temp[4] > 0]
        money = []
        for i in range(len(temp)):
            if temp.iloc[i, 3] == "IH":
                money.append(self.indexpreclose.loc["IH"] * 300 * temp.iloc[i, 4])
            if temp.iloc[i, 3] == "IC":
                money.append(self.indexpreclose.loc["IC"] * 200 * temp.iloc[i, 4])
            if temp.iloc[i, 3] == "IF":
                money.append(self.indexpreclose.loc["IF"] * 300 * temp.iloc[i, 4])
        temp["money"] = money
        self.HedgeConfig = []
        for prod, group in temp.groupby(0):
            group["weight"] = group["money"] / group["money"].sum()
            group[1] = [i.replace("EI", "ZQ") for i in group[1]]
            group[1] = [i.replace("highTVR", "HTVR") for i in group[1]]
            group[1] = [i.replace("hgt", "HGT") for i in group[1]]
            tempResult = pd.DataFrame(index = [prod], columns = list(group[1]))
            tempResult.iloc[0] = list(group["weight"] * 100.0)
            self.HedgeConfig.append(tempResult)

    def work(self, date):
        self.GetHedgeRatio()
        config = []
        for name in ['zyc','dy', 'xp', 'szj']:
            fn = self.configfile.replace("%N", name)
            xl = pd.ExcelFile(fn)
            df = xl.parse('sheet') * 100
            config.append(df)
        config += self.HedgeConfig
        config = pd.concat(config)
        for prod, ratio in config.iterrows():
            if prod not in self.products:
                continue

            prodPath = os.path.join(self.path, prod)
            if not os.path.exists(prodPath):
                os.mkdir(prodPath)
            if not os.path.exists(prodPath + "/datafold"):
                os.mkdir(prodPath + "/datafold")

            confile = prodPath + "/config"
            with open(confile, "w") as fout:
                fout.write("[input]\n")
                fout.write("limit=0.0001\n")
                for model in config.columns:
                    weight = ratio[model]
                    if model=='manual':
                        continue
                    if np.isnan(weight):
                        continue
                    if weight < 0.00001:
                        continue
                    if model not in self.stgpath:
                        raise Exception('invalid model %s in %s' %(model, prod))
                    fout.write("\n")
                    fout.write("weight_%s=%.3f\n" %(model, weight))
                    fout.write("signal_%s=%s\n"   %(model, self.stgpath[model]))
                fout.write("\n")
                fout.write("[output]\n")
                fout.write("outfile={}/datafold/%Y%m%d.csv".format(prodPath))
            self.logger.info("suceed updating config file for {}", prod)

if __name__ == "__main__":
    job = Config()
    job.run()
