import os,sys
import numpy as np
import pandas as pd
from os import system
from MyDB import MyDB

def getAdjprc(dt):
    dbWind = MyDB('WIND_SQL')

    self._conn = pymssql.connect(server="192.168.1.181", user="sa", password="Nm,.hjkl@foresee", database="wind")
    querysql = '''
        declare @trddt varchar(8)
        select @trddt = '%s'

        select trade_days tradedate,rank() over(order by trade_days) cnt
        into #calendar
        from wind.dbo.AshareCalendar
        where s_info_exchmarket ='SSE'

        select *
        ,convert(float,(preclsprc0-xd)/xr) preclsprc
        into #stktrd
        from
        (
        SELECT  left(e.[s_info_windcode], 6) AS stkcode
            , c1.tradedate
            ,e.s_dq_close preclsprc0
            , (ISNULL(bonus_share_ratio, 0) + ISNULL(conversed_ratio, 0) + 1)*ISNULL(consolidate_split_ratio, 1) AS xr
            , ISNULL(cash_dividend_ratio, 0) AS xd
        FROM
            wind.dbo.ashareeodprices e
            join #calendar c0 on e.trade_dt = c0.tradedate
            join #calendar c1 on c1.cnt = c0.cnt + 1
            left join wind.dbo.ASHAREEXRIGHTDIVIDENDRECORD AS P on p.[s_info_windcode]=e.[s_info_windcode] and p.ex_date=c1.tradedate
        WHERE SUBSTRING(e.[s_info_windcode], 1, 1) IN ('0', '3', '6')
            and c1.tradedate = @trddt
        )a

        select e.trade_dt tradedate
        ,(case when S_INFO_WINDCODE='000016.SH' then 'IH'
                     when s_info_windcode='000300.SH' then 'IF'
                     when s_info_windcode='000905.SH' then 'IC'
                end) stkcode
        ,convert(float,S_DQ_CLOSE) preclsprc
        into #idxtrd
        from wind.dbo.AINDEXEODPRICES e
        join #calendar c0 on e.trade_dt = c0.tradedate
        join #calendar c1 on c1.cnt = c0.cnt + 1
        where S_INFO_WINDCODE in ('000016.SH' ,'000300.SH', '000905.SH' )
        and c1.tradedate = @trddt

      ''' % dt

    dbWind.Execute(querysql)

    querysql = '''select stkcode,preclsprc from #idxtrd order by stkcode'''
    dfidx = dbWind.FetchAll(querysql)
    dfidx.set_index('stkcode',inplace=True)
    print(dfidx['preclsprc'])
    return dfidx['preclsprc']

getAdjprc("20200220")
