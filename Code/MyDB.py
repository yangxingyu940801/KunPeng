#import pyodbc
import pymssql
import psycopg2
import pandas as pd

#from Config import DB_CONNECT
class MyDB:
    def __init__(self,name):
        self._name = name
        if(self._name =='WIND_ODBC'):
            self._conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=192.168.1.181;DATABASE=wind;UID=sa;PWD=Nm,.hjkl@foresee')
        elif(self._name =='WIND_SQL'):
            self._conn = pymssql.connect(server="192.168.1.181", user="sa", password="Nm,.hjkl@foresee", database="wind")
        elif(self._name=='AU_PG'):
            self._conn = psycopg2.connect(database="freiburg", user="dany", password="KhalDrogo", host="192.168.2.168",port="5432")


    def __del__(self):
        self._conn.close()

    def getCursor(self):
        return self._conn.cursor();

    def Commit(self):
        self._conn.commit()

    def Execute(self,exesql,bcommit = False):
        cur = self.getCursor()
        cur.execute(exesql)
        if(bcommit == True):
            self.Commit()

    def FetchAll(self, querysql):
        cur = self.getCursor()
        cur.execute(querysql)

        cols = [i[0] for i in cur.description]
        result = cur.fetchall()
        df_result= pd.DataFrame(dict(zip(cols, row)) for row in result)

        return df_result

def getAdjprc(dt):
    dbWind = MyDB('WIND_SQL')

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
    return dfidx['preclsprc']


if __name__=="__main__":
    a = getAdjprc("20200220")
    print(type(a))
