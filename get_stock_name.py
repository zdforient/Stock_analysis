from pathlib import Path
import pandas as pd
def load_stock_name():
    current_path = Path().absolute()
    data_path = current_path.parent.parent / 'data' / 'info' / 'companylist.csv'
    full_data = pd.read_csv(data_path)
    company_name = full_data.iloc[:,0]
    return company_name

#cn = load_stock_name()
#print(cn)
