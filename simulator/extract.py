import yfinance as yf
from get_stock_name import load_stock_name
from pathlib import Path
import pandas as pd

# load full datasets of periods and intervals
def load_stock_data(duration = '2y', interval = '1d'):
    current_path = Path().absolute()
    csv_name = duration+'_'+interval+'.csv'
    data_path = current_path.parent.parent / 'data' / 'stock_history_data' / csv_name
    if data_path.exists():
        return pd.read_csv(data_path,index_col=0)
    
    
    stock_name = load_stock_name()
    stock_data_list = []
    stock_name = stock_name[0:len(stock_name):1]
    stock_open_data = pd.DataFrame()
    for i in range(len(stock_name)):
        name = stock_name.iloc[i]
        stock_data_i = yf.Ticker(name).history(period = duration, interval = interval)
        if stock_data_i.empty or stock_data_i.shape[0] < 10:
           continue
        stock_data_i.rename({'Open':name},axis=1,inplace=True)
        #stock_data_i.reset_index(drop=True)
        try:
            #stock_open_data = pd.concat([stock_open_data, stock_data_i.loc[:,name]], ignore_index=True,axis=1)
            stock_open_data = stock_open_data.join(stock_data_i.loc[:,name],how='outer')
        except:
            print(name)
        #stock_data_list.append(stock_data_i.iloc[:,0])
    #stock_open_data = pd.concat(stock_data_list,axis=1)
    #stock_open_data.columns = stock_name
    stock_open_data = stock_open_data[~stock_open_data.index.duplicated(keep='first')]
    stock_open_data.to_csv(data_path, header = 1)#, index = False

        
    #print(stock_open_data)
    #print(data_path)
    #print(data_path.parent.exists())
    
    return stock_open_data

#select ROA > 1.4 from sep 2020
def get_ROA_stock(duration = '2y', interval = '1d'):
    current_path = Path().absolute()
    csv_name = duration+'_'+interval+'_ROA.csv'
    data_path = current_path.parent.parent / 'data' / 'stock_history_data' / csv_name
    #if data_path.exists():
        #return pd.read_csv(data_path,index_col=0)        
    stock_data = load_stock_data(duration, interval)
    stock_data = stock_data[~stock_data.index.duplicated(keep='first')]
    #select ROA (value[-1] > value[0] * 2 || value[-1] > 1.4 * value[1/2])
    ROA_stock_num = []
    rown, coln = stock_data.shape[0], stock_data.shape[1]
    rown_half = (int) (rown / 2)
    for i in range(coln):
        if (stock_data.iloc[rown-1,i] > 1.4 * stock_data.iloc[rown_half,i] or
           stock_data.iloc[rown-1,i] > 2 * stock_data.iloc[0,i]):
            ROA_stock_num.append(i)
    ROA_stock_data = stock_data.iloc[:,ROA_stock_num]
    ROA_stock_data.to_csv(data_path, header = 1)
    return ROA_stock_data
    #print(data)

def clean(data):
    rowsum = data.sum(axis=1)
    data = data.fillna(-1)
    data = data.drop(data.index & rowsum[rowsum<1].index)
        

#get_ROA_stock('2y', '1d')
#data = load_stock_data('1mo','1d')
 
