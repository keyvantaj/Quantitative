from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import TickTypeEnum
from ibapi.common import * #for TickerId type

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep, strftime, localtime,time 

sleeptime = 3

# Read Data
#########################################################
#########################################################

def read_ohlcv(reqId, symbol, sec_type, exch, prim_exch, curr, durationStr, barSizeSetting):

    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exch
    contract.primaryExchange = prim_exch
    contract.currency = curr

    class TestApp(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self,self)

            self.historicaldata = pd.DataFrame([], columns = ['Open', 'High', 'Low', 'Close', 'Volume'])
            

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
            
        def historicalData(self,reqId, bar):

            self.historicaldata.index.name = 'Date'
            self.historicaldata.loc[bar.date] = bar.open, bar.high, bar.low, bar.close, bar.volume 

        def historicalDataEnd(self, reqId: int, start: str, end: str):
            super().historicalDataEnd(reqId, start, end)
            print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
            self.disconnect()
            

        
    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)
    
    app.reqHistoricalData(reqId = reqId, 
                            contract = contract, 
                            endDateTime = '', 
                            durationStr = durationStr, 
                            barSizeSetting = barSizeSetting, 
                            whatToShow = 'TRADES',
                            useRTH = 1, # =1 for RTH data
                            formatDate = 1,
                            keepUpToDate = False,
                            chartOptions = [])
        
    ohlcv = app.historicaldata
    app.run()
    print ('Creating OHLCV dataframe ...')
    sleep(sleeptime)
    
    return ohlcv


def read_scanner(reqId, numberOfRows, instrument, locationCode, abovePrice,
                       aboveVolume, belowPrice, marketCapAbove, marketCapBelow, 
                       moodyRatingAbove, moodyRatingBelow, spRatingAbove, spRatingBelow, scanCode):

    scanSub = ScannerSubscription()
    scanSub.numberOfRows = numberOfRows
    scanSub.instrument = instrument
    scanSub.locationCode = locationCode
    scanSub.abovePrice = abovePrice
    scanSub.aboveVolume = aboveVolume 
    scanSub.belowPrice = belowPrice
    scanSub.marketCapAbove = marketCapAbove
    scanSub.marketCapBelow = marketCapBelow
    scanSub.moodyRatingAbove = moodyRatingAbove
    scanSub.moodyRatingBelow = moodyRatingBelow
    scanSub.spRatingAbove = spRatingAbove
    scanSub.spRatingBelow = spRatingBelow    
    scanSub.scanCode = scanCode

    class TestApp(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self,self)

            self.scannerdata = pd.DataFrame(index = [], columns = ['Symbol', 'SecType' , 'Currency', 'primaryExchange',                                                                      'exchange', 'Distance', 'Benchmark', 'Projection', 'Legs String'])

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

        def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
            super().scannerData(reqId, rank, contractDetails, distance, benchmark,projection, legsStr)
            self.scannerdata.index.name = 'Rank'
            self.scannerdata.loc[rank] = [contractDetails.contract.symbol, contractDetails.contract.secType, contractDetails.contract.currency, contractDetails.contract.primaryExchange, contractDetails.contract.exchange, distance, benchmark, projection, legsStr] 

        def scannerDataEnd(self, reqId: int):
            print("ScannerDataEnd. ReqId:", reqId)
            self.disconnect()

    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)      

    app.reqScannerSubscription(reqId = reqId, subscription = scanSub,
                          scannerSubscriptionOptions = [],
                          scannerSubscriptionFilterOptions = [])

    scanner = app.scannerdata
    
    app.run()
    sleep(sleeptime)
        
    return scanner

def read_fundamental(reqId, symbol, sec_type, exch, prim_exch, curr,reportType):
    

    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exch
    contract.currency = curr
    contract.primaryExchange = prim_exch
    
    class TestApp(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self,self)
                                      
            self.fund = []
    
        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
        
        def fundamentalData(self, reqId: TickerId, data: str):
            super().fundamentalData(reqId, data)
            print ('Reading XML data ...')
            parser = BeautifulSoup(data, 'lxml')
            self.fund.append(parser)
            self.disconnect()

    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)      
    app.reqFundamentalData(reqId = reqId,
                           contract = contract, 
                           reportType = reportType, 
                           fundamentalDataOptions = [])

    fund = app.fund
    app.run()
    sleep(sleeptime)
    return fund[0]



def parse_resc(parser):
    
    print ('Parsing resc data started ...')
    resc = pd.DataFrame(index = [parser.find('name').text],
                        columns = ['Exchange', 'Symbol', 'Sector', 'CLPRICE', 'SHARESOUT',
                                   'MARKETCAP', '52WKHIGH', '52WKLOW'])
    resc_ann = pd.DataFrame()
    resc_q = pd.DataFrame()
    
    resc.iloc[:,0] = parser.find('exchange').text
    resc.iloc[:,1] = parser.findAll('secid')[2].text
    resc.iloc[:,2] = parser.findAll('sector')[0].text

    resc.iloc[:,3] = parser.findAll('marketdataitem')[0].text
    resc.iloc[:,4] = parser.findAll('marketdataitem')[1].text
    resc.iloc[:,5] = parser.findAll('marketdataitem')[2].text
    resc.iloc[:,6] = parser.findAll('marketdataitem')[3].text
    resc.iloc[:,7] = parser.findAll('marketdataitem')[4].text
    #resc.iloc[:,9] = parser.findAll('fyactual')[0].text
    
    annual = [];columns = [];quarter = []
    for item in parser.findAll('fyactual'):
        columns.append(item['type'].split()[0])
        for per in item.findAll('fyperiod'):
            if per['periodtype'] == 'A':
                annual.append(per['fyear'])
            if per['periodtype'] == 'Q':
                quarter.append('{}-{}'.format(per['endcalyear'],per['endmonth']))
    
    index = list(set(annual))
    index_q = list(set(quarter))
    resc_ann = pd.DataFrame(index = index, columns = columns).sort_index(axis = 0,ascending = False)
    resc_q = pd.DataFrame(index = index_q, columns = columns).sort_index(axis = 0,ascending = False)
    
    for item in parser.findAll('fyactual'):
        for per in item.findAll('fyperiod'):
            
            if per['periodtype'] == 'Q':
                try:
                    resc_q.loc['{}-{}'.format(per['endcalyear'],per['endmonth']),item['type'].split()[0]] = float(per.find('actvalue').text)
                except:
                    resc_q.loc['{}-{}'.format(per['endcalyear'],per['endmonth']),item['type'].split()[0]] = np.nan  
                    
            if per['periodtype'] == 'A':
                try:
                    resc_ann.loc[per['fyear'],item['type'].split()[0]] = float(per.find('actvalue').text)
                except:
                    resc_ann.loc[per['fyear'],item['type'].split()[0]] = np.nan
                    
    return resc, resc_ann, resc_q

def parse_reportsnapshot(parser):

    print ('Parsing reportsnapshot data started...')
    business_summary = parser.findAll('text')[0].text
    brief = parser.findAll('text')[1].text
    
    try:
        s0 = parser.find('contactinfo').find('streetaddress').text,
        s1 = parser.find('contactinfo').find('city').text,
        s2 = parser.find('contactinfo').find('state-region').text,
        s3 = parser.find('contactinfo').find('country').text
    except:
        s0 = np.nan; s1 = np.nan; s2 = np.nan; s3 = np.nan
    
    address = '{},{},{},{}'.format(s0,s1,s2,s3)
    
    try:
        name = parser.findAll('coid')[1].text
    except:
        name = np.nan
    try:
        ct =  parser.find('cotype').text
    except:
        ct = np.nan
    try:
        desc = parser.findAll('issue')[0]['desc']
    except:
        desc = np.nan
    try:
        exc = parser.findAll('exchange')[0].text
    except:
        exc = np.nan
    try:
        ind = parser.findAll('industry')[0].text
    except:
        ind = np.nan
    try:
        index = parser.find('indexconstituet').text
    except:
        index = np.nan
    
    snap = pd.DataFrame(index = [name],
                        data = {'Company Type':ct,
                                'Desc':desc,
                                'Exchange':exc ,
                                'Industry':ind,
                                'Index': index})
    dicted = {};dicted_est = {}
    for i in range(len(parser.find('ratios').findAll('ratio'))):
        try:
            dicted[parser.find('ratios').findAll('ratio')[i]['fieldname']] = float(parser.find('ratios').findAll('ratio')[i].text)
        except:
            dicted[parser.find('ratios').findAll('ratio')[i]['fieldname']] = parser.find('ratios').findAll('ratio')[i].text
            
    ratio = pd.DataFrame(index = [parser.findAll('coid')[1].text], data = dicted)
    
    for i in range(len(parser.find('forecastdata').findAll('ratio'))):
        try:
            dicted_est[parser.find('forecastdata').findAll('ratio')[i]['fieldname']] = float(parser.find('forecastdata').findAll('ratio')[i].text)
        except:
            dicted_est[parser.find('forecastdata').findAll('ratio')[i]['fieldname']] = parser.find('forecastdata').findAll('ratio')[i].text
            
    estimate = pd.DataFrame(index = [parser.findAll('coid')[1].text], data = dicted_est)
    
    return snap, estimate, brief, business_summary, address
    
def parse_reportsfinsummary(parser):
        
    print ('Parsing reportsfinsummary data started...')
    
    date_div = [];data_div = []
    
    for i in parser.findAll('dividendpershare'):
        if i['period'] == '12M' and i['reporttype'] == 'TTM':
            
            date_div.append(i['asofdate'])
            try:
                data_div.append(float(i.text))
            except:
                data_div.append(np.nan)
                
    data_rev = []
    for i in parser.findAll('totalrevenue'):
        if i['period'] == '12M' and i['reporttype'] == 'TTM':
            try:
                data_rev.append(float(i.text))
            except:
                data_rev.append(np.nan)
                
    data_eps = []
    for i in parser.findAll('eps'):
        if i['period'] == '12M' and i['reporttype'] == 'TTM':
            try:
                data_eps.append(float(i.text))
            except:
                data_eps.append(np.nan)

    fin = pd.DataFrame(index = date_div,
                       data = {'Dividend Per Share(TTM)':data_div,
                               'Total Revenue(TTM)':data_rev, 
                               'EPS(TTM)':data_eps}).sort_index(axis = 0,ascending = False)
    return fin

def parse_reportsfinstatements(parser):
    
    print ('Parsing reportsfinstatements data started...')
    mapp = dict()
    for item in parser.findAll('mapitem'):
        mapp[item['coaitem']] = item.text
        
    
    #ANNUAL
    index = [];columns = []
    for item in parser.findAll('annualperiods')[0].findAll('fiscalperiod'):
        index.append(datetime.strptime(item['fiscalyear'], '%Y').year)
    
    for i in parser.findAll('annualperiods')[0].findAll('fiscalperiod')[0].findAll('lineitem'):
        columns.append(mapp[i['coacode']])

    annual = pd.DataFrame(index = index, columns = columns)
    annual.index.name = 'Annual'
    for item in parser.findAll('annualperiods')[0].findAll('fiscalperiod'):
        for i in item.findAll('lineitem'):
            try:
                annual.loc[datetime.strptime(item['fiscalyear'], '%Y').year,mapp[i['coacode']]] = float(i.text)
            except:
                annual.loc[datetime.strptime(item['fiscalyear'], '%Y').year,mapp[i['coacode']]] = np.nan
        
    # QUARTER
    index_q = [];columns_q = []
    for item in parser.findAll('interimperiods')[0].findAll('fiscalperiod'):
        index_q.append(datetime.strptime(item['enddate'], '%Y-%m-%d').date())
    
    for i in parser.findAll('interimperiods')[0].findAll('fiscalperiod')[0].findAll('lineitem'):
        columns_q.append(mapp[i['coacode']])

    quarter = pd.DataFrame(index = index_q, columns = columns_q)
    quarter.index.name = 'Quarter'
    for item in parser.findAll('interimperiods')[0].findAll('fiscalperiod'):
        for i in item.findAll('lineitem'):
            try:
                quarter.loc[datetime.strptime(item['enddate'], '%Y-%m-%d').date(),mapp[i['coacode']]] = float(i.text)
            except:
                quarter.loc[datetime.strptime(item['enddate'], '%Y-%m-%d').date(),mapp[i['coacode']]] = np.nan
                
    return quarter, annual

# DataFrame
#########################################################
#########################################################   

def create_info_dataframe(universe, historical_data):
    
    print ('Creating historical information dataframe...')
    
    sector = pd.DataFrame(index = historical_data.index , columns = universe)
    exchange = pd.DataFrame(index = historical_data.index , columns = universe)
    name = pd.DataFrame(index = historical_data.index , columns = universe)
    indx = pd.DataFrame(index = historical_data.index , columns = universe)
    desc = pd.DataFrame(index = historical_data.index , columns = universe)
    comptype =  pd.DataFrame(index = historical_data.index , columns = universe)
    bs = {}
    
    for i,tick in enumerate(universe):
     
        RESC = read_fundamental(reqId = i,
                                 symbol = tick, 
                                 sec_type = 'STK', 
                                 exch = 'SMART', 
                                 prim_exch = 'NASDAQ', 
                                 curr = 'USD',
                                 reportType = 'RESC')

        reportsnapshot = read_fundamental(reqId=i,
                                 symbol = tick, 
                                 sec_type = 'STK', 
                                 exch = 'SMART', 
                                 prim_exch = 'NASDAQ', 
                                 curr = 'USD',
                                 reportType = 'ReportSnapshot')

        resc, resc_ann, resc_q = parse_resc(parser = RESC)
        snap, estimate, brief, business_summary, address = parse_reportsnapshot(parser = reportsnapshot)
        bs[tick] = [business_summary,address,brief]
        
        for date in historical_data.index:

            try:
                sector.loc[date,tick] = resc['Sector'][0]
            except:
                sector.loc[date,tick] = np.nan
            try:
                exchange.loc[date,tick] = resc['Exchange'][0]
            except:
                exchange.loc[date,tick] = np.nan
            try:
                name.loc[date,tick] = resc.index[0]
            except:
                name.loc[date,tick] = np.nan
            try:
                indx.loc[date,tick] = snap['Index'][0]
            except:
                indx.loc[date,tick] = np.nan 
            try:
                desc.loc[date,tick] = snap['Desc'][0]
            except:
                desc.loc[date,tick] = np.nan 
            try:
                comptype.loc[date,tick] = snap['Company Type'][0]
            except:
                comptype.loc[date,tick] = np.nan
    
    return sector, exchange, name, indx, bs, desc, comptype

def create_factor_dataframe(universe, historical_data, factors):
    
    result = {}
    
    for factor in factors:

        df = pd.DataFrame(index = historical_data.index,data = [], columns = universe)
        
        for i,tick in enumerate(universe):
            print ('Creating {} dataframe for {}'.format(factor,tick))
            
            reportsfinstatements = read_fundamental(reqId = i,
                                 symbol = tick, 
                                 sec_type = 'STK', 
                                 exch = 'SMART', 
                                 prim_exch = 'NASDAQ', 
                                 curr = 'USD',
                                 reportType = 'ReportsFinStatements')

            quarter, annual = parse_reportsfinstatements(parser = reportsfinstatements)
            
            for date in historical_data.index:

                try:

                    if int(datetime.strptime(str(date), "%Y%m%d").timestamp()) >= int(datetime.strptime(str(quarter.index[0]), '%Y-%m-%d').timestamp()):
                        try:
                            df.loc[date,tick] = quarter.loc[quarter.index[0],factor]
                        except:
                            df.loc[date,tick] = np.nan                

                    elif int(datetime.strptime(str(date), "%Y%m%d").timestamp()) < int(datetime.strptime(str(quarter.index[0]), '%Y-%m-%d').timestamp()) and int(datetime.strptime(str(date), "%Y%m%d").timestamp()) >= int(datetime.strptime(str(quarter.index[1]), '%Y-%m-%d').timestamp()):
                        try:
                            df.loc[date,tick] = quarter.loc[quarter.index[1],factor]
                        except:
                            df.loc[date,tick] = np.nan 

                    elif int(datetime.strptime(str(date), "%Y%m%d").timestamp()) < int(datetime.strptime(str(quarter.index[1]), '%Y-%m-%d').timestamp()) and int(datetime.strptime(str(date), "%Y%m%d").timestamp()) >= int(datetime.strptime(str(quarter.index[2]), '%Y-%m-%d').timestamp()):
                        try:
                            df.loc[date,tick] = quarter.loc[quarter.index[2],factor]
                        except:
                            df.loc[date,tick] = np.nan            


                    elif int(datetime.strptime(str(date), "%Y%m%d").timestamp()) < int(datetime.strptime(str(quarter.index[2]), '%Y-%m-%d').timestamp()) and int(datetime.strptime(str(date), "%Y%m%d").timestamp()) >= int(datetime.strptime(str(quarter.index[3]), '%Y-%m-%d').timestamp()):
                        try:
                            df.loc[date,tick] = quarter.loc[quarter.index[3],factor]
                        except:
                            df.loc[date,tick] = np.nan 


                    elif int(datetime.strptime(str(date), "%Y%m%d").timestamp()) < int(datetime.strptime(str(quarter.index[3]), '%Y-%m-%d').timestamp()) and int(datetime.strptime(str(date), "%Y%m%d").timestamp()) >= int(datetime.strptime(str(quarter.index[4]), '%Y-%m-%d').timestamp()):
                        try:
                            df.loc[date,tick] = quarter.loc[quarter.index[4],factor]
                        except:
                            df.loc[date,tick] = np.nan    
                except:
                    df.loc[date,tick] = np.nan
            
        result[factor] = df
    return result

def create_technical_dataframe(universe, historical_data, duration):
    print ('Creating historical technical dataframe...')
    
    close = pd.DataFrame(index = historical_data.index , columns = universe)
    openn = pd.DataFrame(index = historical_data.index , columns = universe)
    high = pd.DataFrame(index = historical_data.index , columns = universe)
    low = pd.DataFrame(index = historical_data.index , columns = universe)
    volume = pd.DataFrame(index = historical_data.index , columns = universe)
    
    for tick in universe:
        print ('{}'.format(tick))
        ohlcv = read_ohlcv(reqId = 0,
                             symbol = tick, 
                             sec_type = 'STK', 
                             exch = 'SMART', 
                             prim_exch = 'NASDAQ', 
                             curr = 'USD',
                             durationStr = duration,
                             barSizeSetting = '1 day')
        
        close[tick] = ohlcv['Close']
        openn[tick] = ohlcv['Open']
        low[tick] = ohlcv['Low']
        high[tick] = ohlcv['High']
        volume[tick] = ohlcv['Volume']
        
    return openn, high, low, close, volume
        
        
        

def create_multiindex_factor_dataframe(universe, historical_data, factors):
    
    start_time = time()
    print ('Fetching data into multiindex dataframe...')
    result = []
    result_dict = create_factor_dataframe(universe, historical_data, factors)
    sector, exchange, name, indx, bs, desc, comptype = create_info_dataframe(universe, historical_data)
    openn, high, low, close, volume = create_technical_dataframe(universe, historical_data)
    
    for factor in factors:

        df = result_dict[factor].stack().to_frame(factor)
        result.append(df)
    
    sector = sector.stack().to_frame('Sector')
    exchange = exchange.stack().to_frame('Exchange')
    name = name.stack().to_frame('Name')
    comptype = comptype.stack().to_frame('Company Type')
    desc = desc.stack().to_frame('Desc') 
    indx = indx.stack().to_frame('Index')
    volume = volume.stack().to_frame('Volume')
    close = close.stack().to_frame('Close')
    
    result.append(close)
    result.append(volume)
    result.append(sector)
    result.append(exchange)
    result.append(name)
    result.append(indx)
    result.append(desc)
    result.append(comptype)
     
    final = pd.concat(result,axis=1)
    final.index.levels[1].name = 'Symbol'    
    print("--- %s seconds ---" % (time() - start_time))
    
    return final,bs  


#ORDERS
#########################################################
#########################################################   

def read_nextvalidid(reqId):

    class TestApp(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self,self)

            self.nextValidOrderId = []
            

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
            
        def nextValidId(self,orderId):
            super().nextValidId(orderId)
            self.nextValidOrderId.append(orderId)
            print("NextValidId:", orderId)
            self.disconnect()
           
    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)
    
    app.reqIds(-1)
    nid = app.nextValidOrderId
        
    app.run()
    sleep(sleeptime)
    
    return nid[0]

def placing_orders(orderId, reqId, symbol, sec_type, exch, prim_exch, curr, order_type, quantity, action, positions):
    
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exch
    contract.primaryExchange = prim_exch
    contract.currency = curr
    
    order = Order()
    order.orderType = order_type
    order.totalQuantity = quantity
    order.action = action

    class TestApp(EWrapper, EClient):

        def __init__(self):
            EClient.__init__(self,self)

        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)

    if contract.symbol in positions.index:
        order.totalQuantity = int(order.totalQuantity) - int(positions.loc[contract.symbol,'Position'])
        app.placeOrder(orderId = orderId, contract = contract, order = order)
        print ('{} positions of {} already in portfolio '.format(positions.loc[contract.symbol,'Position'],contract.symbol))
        print ('New order quantity placed is: {}'.format(order.totalQuantity))
        
    else:
        app.placeOrder(orderId = orderId, contract = contract, order = order)
        print ('order quantity placed for {} is: {} '.format(contract.symbol, order.totalQuantity))
        
    sleep(sleeptime)
    
    return order, contract

    app.disconnect()
    app.run()


def read_positions(subscribe, acctCode):
    
    class TestApp(EWrapper, EClient):


        def __init__(self):
            EClient.__init__(self,self)
            self.up = pd.DataFrame([], columns = ['Position', 'marketPrice', 'marketValue', 'averageCost', 'unrealizedPNL', 'realizedPNL'])
            
            
        def error(self, reqId:TickerId, errorCode:int, errorString:str):
            if reqId > -1:
                print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
            
        def updatePortfolio (self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
            self.up.index.name = 'Symbol'            
            self.up.loc[contract.symbol] = position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL
                        
        def positionEnd(self):
            super().positionEnd()
            print("PositionEnd")
            self.disconnect()

            
    app = TestApp()
    app.connect('127.0.0.1', 7497, 0)
    
    app.reqAccountUpdates(subscribe = subscribe,acctCode = acctCode)
    app.reqPositions()
    
    update = app.up
    
    app.run()
    
    sleep(sleeptime)
    print ('Reading Portfolio')
    return update

#PREPROCESSING
#########################################################
######################################################### 

def cleaning_multiindex_dataframe(df, pernan_to_drop):
    print ('Cleaning data')

    subset = df.select_dtypes(exclude=[np.float, np.int])
    col_len = len(subset.columns)

    df = df.iloc[:,:-col_len]
    df_cleaned = df.apply(pd.to_numeric, errors='coerce')
    df_cleaned.replace([0,-1], np.nan, inplace=True)

    total = df_cleaned.isna().sum().sort_values(ascending=False)
    percent = (df_cleaned.isna().sum()/df_cleaned.isna().count()).sort_values(ascending=False)
    nan_df_cleaned = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

    f, ax = plt.subplots(figsize=(20, 10))

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(5)
        plt.xticks(rotation='90')

    sns.barplot(x=nan_df_cleaned.index, y=nan_df_cleaned['Percent'])
    plt.xlabel('Features', fontsize=15)
    plt.ylabel('Percent of nan values', fontsize=15)
    plt.title('Percent nan data by feature dataset', fontsize=15)
    plt.show()

    features_to_drop = nan_df_cleaned[nan_df_cleaned['Percent']>pernan_to_drop].index
    df_cleaned_dropna = df_cleaned.drop(features_to_drop, axis=1)


    print ('The percentage of dataframe dropped columns is {}%.'.format(int(((df_cleaned.shape[1] - df_cleaned_dropna.shape[1])/df_cleaned.shape[1])*100)))

    clean_df_fillna = df_cleaned_dropna.fillna(-1)

    return clean_df_fillna

def demean_multiindex(df):
    
    df_demean = df - df.mean(axis = 0, level = 0)

    return df_demean

def demean(df):
    
    df_demean = df.subtract(df.mean(axis=1), axis=0)

    return df_demean
    
def normalize_multiindex(df):
    
    df_norm = (df - df.min(axis = 0, level = 0)) / (df.max(axis = 0, level = 0) - df.min(axis = 0, level = 0))

    return df_norm

def rank_multiindex(df, ascending=False):
    
    ranked = df.groupby(level=0).rank(ascending=ascending)

    return ranked

def zscore(df):
    
    dfz = (df - df.mean(axis = 0))/df.std(axis = 0,ddof=0) 
    
    return dfz    
    