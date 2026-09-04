import pandas as pd 
import matplotlib.pyplot  as plt 
import os 

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Islamic_Companies_Data.xlsx")

companies = pd.read_excel(   
     file_path, 
     sheet_name= 'companies' , engine= 'openpyxl'
)

financials = pd.read_excel (
         file_path, 
        sheet_name= 'financials' , engine= 'openpyxl'
)

stock_prices= pd.read_excel (    
    file_path,
    sheet_name= 'stock_prices' , engine= 'openpyxl'
)
dividends = pd.read_excel (
        file_path,
        sheet_name= 'dividends' , engine= 'openpyxl'
)


prices_copy = stock_prices.copy() 
prices_copy = prices_copy.sort_values('price_date')
prices_copy['price_date'] = pd.to_datetime(prices_copy['price_date'])
latest_prices = prices_copy.sort_values('price_date').groupby('company_id').last().reset_index()
latest_prices = latest_prices[['company_id', 'closing_price']]


dividends['dividend_date'] = pd.to_datetime(dividends['dividend_date'])
latest_dividends = dividends.sort_values('dividend_date').groupby('company_id').last().reset_index()
latest_dividends = latest_dividends[['company_id', 'dividend_per_share']]

full = pd.merge(companies, financials, on='company_id', how='left')
full = pd.merge(full, latest_prices, on='company_id', how='left')
full = pd.merge(full, latest_dividends, on='company_id', how='left')

prices_copy = stock_prices.copy() 
prices_copy = prices_copy.sort_values('price_date')
prices_copy['daily_return'] = prices_copy.sort_values('price_date').groupby('company_id')['closing_price'].pct_change()
volatility_df = prices_copy.groupby('company_id')['daily_return'].std().reset_index()
volatility_df.columns = ['company_id', 'Volatility']

full = pd.merge(full, volatility_df, on='company_id', how='left')

full['P_E_Ratio'] = full['closing_price'] /full['earnings_per_share']
full['ROE'] = (full['net_income'] / full['equity'] * 100)

full=full[full['is_sharia_compliant'] == 1 ]
full = full.set_index('company_id')


def evaluate_invest(row):
    P_E_Ranking = 'undervalued' if row['P_E_Ratio'] <= 15 else ('Fair_value' if row['P_E_Ratio'] <= 25 else 'Overvalued')
    ROE_ranking = 'HIGH' if row['ROE'] >= 20  else ('MED' if row['ROE'] >= 15 else 'LOW')
    Volatility_Ranking = 'Low Rink' if row['Volatility'] < 0.1 else ('Medium Risk' if row['Volatility'] <= 0.2 else 'High Risk')

    return f'Stock_Ranking : {P_E_Ranking} | ROE_Ranking : {ROE_ranking} | Volatility_Ranking : {Volatility_Ranking} '

full['Ranking'] = full.apply(evaluate_invest , axis= 1 )

def ranking_by_points(row):
    score = 0
    if row['P_E_Ratio'] <= 15: score += 1
    if row['ROE'] >= 20: score += 1
    if row['Volatility'] < 0.1: score += 1
    return f'Ranking_by_points: {score}/3'

full['P_Ranking']= full.apply(ranking_by_points , axis= 1)

plt.figure(figsize=(10, 6))
plt.scatter(full['P_E_Ratio'], full['ROE'], color='navy', alpha=0.7, edgecolors='black')
plt.title('Stock Analysis: ROE vs P/E Ratio')
plt.xlabel('P/E Ratio ')
plt.ylabel('ROE % ')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print(full)
