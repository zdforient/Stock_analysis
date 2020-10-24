import yfinance as yf
import pandas as pd
from pathlib import Path
#from extract import get_ROA_stock

class SIM:

    def __init__(self, backlen = 100, freq = 3, stock_num = 5, total_input = 1000, timelen = '2y'):
        self.freq = freq
        self.stock_num = stock_num
        self.initial_input = total_input
        self.cur_invest = self.initial_input
        self.data_path = Path().absolute().parent / 'data'
        self.extract_module_path = Path().absolute().parent / 'simulator'
        self.selected_stock = pd.Index
        self.invest_ratio = pd.DataFrame()
        self.prof_ratio = pd.DataFrame()
        self.stock_data = pd.DataFrame()
        self.ROA_data = pd.DataFrame()
        self.backlen = backlen
        self.timelen = timelen
        
    def one_step(self,t0,method='noob'):
        
        if method == 'noob':
            self.select_stock_noob(t0)
        elif method == '3factor':
            self.select_stock_3factor(t0)
        elif method == '5factor':
            self.select_stock_5factor(t0)
        elif method == '1934':
            self.select_stock_1943(t0)
        selected_stock_data = self.ROA_data[self.ROA_data.columns & self.selected_stock]
        self.prof_ratio = selected_stock_data.iloc[t0+self.freq]/selected_stock_data.iloc[t0]
        self.cur_invest *= sum(self.invest_ratio*self.prof_ratio)
        
    def clean(self, data):
        rowsum = data.sum(axis=1)
        data = data.fillna(-1)
        data = data.drop(data.index & rowsum[rowsum<1].index)
        return data
        #data = data.fillna(-1)     
             

    def load_data(self):
        ROA_data_path = self.data_path / 'stock_history_data' / (self.timelen + '_1d_ROA.csv')
        #ROA_data = get_ROA_stock()
        self.ROA_data = pd.read_csv(self.data_path / 'stock_history_data' / (self.timelen + '_1d_ROA.csv'),index_col=0)
        #self.stock_data = pd.read_csv(self.data_path / 'stock_history_data' / '10y_1d.csv',index_col=0)
        self.ROA_data = self.clean(self.ROA_data)
        #self.clean(self.stock_data)
        



    def select_stock_noob(self, t0):
        #may use caldendar module: https://docs.python.org/3/library/calendar.html
        row0, row1 = self.ROA_data.iloc[t0-self.freq], self.ROA_data.iloc[t0]
        row0.sort_values()
        row1.sort_values()
        row0 = row0[row0<1e3]
        row0 = row0[row0>1]
        row1 = row1[row1<1e3]
        row1 = row1[row1>1]
        row2 = row1 / row0
        row2 = row2.sort_values(ascending=False)
        row2 = row2.drop(row2[row2>pow(2,self.freq*4)])
        #print(row2)
        row2 = row2[0:self.stock_num]
        #print(row2)
        ratio = row2*0.5 - 0.5
        ratio /= row2
        s = sum(ratio)
        ratio /= s
        self.invest_ratio = ratio
        self.selected_stock = row2.index

    def select_stock_1943(self, t0):
        rown, coln = self.ROA_data.shape[0], self.ROA_data.shape[1]
        
        y0 = (int) (rown / 2)
        y1 = rown - 1
        '''
        y1 = (int) (rown / 2)
        y0 = 10
        '''
        stock_price_now = self.ROA_data.iloc[t0]
        stock_price_last = self.ROA_data.iloc[t0-self.backlen]
        stock_return = stock_price_now - stock_price_last
        pe = stock_return / stock_price_now
        #ep = 1.0/pe
        pe = pe.fillna(0)
        pe_avg = max(0, sum(pe) / coln)
        #ep_avg = sum(ep) / coln
        double_pe_data = pe
        price_data = stock_price_now.sort_values(ascending=False)
        price_data = price_data[int(coln*0.33):int(coln*0.9)]
        price_data = price_data[price_data < 10]
        price_data = price_data[price_data > 1]

        
        quality = double_pe_data[price_data.index&double_pe_data.index]
        sort_quality = quality.sort_values(ascending=False)
        sort_quality = sort_quality[sort_quality>0]
        sort_quality = sort_quality[0:self.stock_num]
        #print('#####################',sum(pe), coln)

        self.selected_stock = sort_quality.index
        self.invest_ratio = sort_quality / sum(sort_quality)


        
    def show_status(self):
        print("Principle: \n", self.cur_invest)
        print("selected_stock: \n", self.selected_stock)
        print("invest_ratio: \n", self.invest_ratio)
        print("prof_ratio: \n", self.prof_ratio)

    def Test_sim(self, method = 'noob',show = 0):
        t0 = self.backlen
        self.load_data()
        #print('simulation started:')
        print('freq: ', self.freq, '\nDate: ', self.ROA_data.index[t0])
        #print("Initial input: \n", self.cur_invest)
        while t0 < self.ROA_data.shape[0]- self.freq - 1 and self.cur_invest>10:
            self.one_step(t0, method)
            if show:
                self.show_status()
                #print('t0: ',t0)
            t0 += self.freq
            #
        print("Principle: \n", self.cur_invest)
        #print("End date: \n", self.ROA_data.index[t0])
        

            

            








        
        
