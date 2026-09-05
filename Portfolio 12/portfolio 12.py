import pandas as pd 
import matplotlib.pyplot as plt 



New_companies = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\12\companies_metrics_raw.xlsx' , 
    engine='openpyxl'
) 
New_companies.columns = New_companies.columns.str.strip()

Old_companies = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Eleventh\Portfolio_11.xlsx',
    engine='openpyxl'
)
Old_companies.columns = Old_companies.columns.str.strip()


#----
PE_average = New_companies['PE_Ratio'].mean()
ROE_average = New_companies['ROE (%)'].mean()
DY_average = New_companies['Dividend_Yield (%)'].mean()
#-----
New_companies['PE_Ratio'] = New_companies['PE_Ratio'].fillna(PE_average).round(0)
New_companies['ROE (%)'] = New_companies['ROE (%)'].fillna(ROE_average).round(0)
New_companies['Dividend_Yield (%)'] = New_companies['Dividend_Yield (%)'].fillna(DY_average).round(0)
#---
if 'Company Name' in New_companies.columns and 'Company Name' in Old_companies.columns:
    New_companies = New_companies.drop(columns=['Company Name'])
    

All_companies = pd.merge(Old_companies , New_companies , on= 'Company_ID' , how= 'left')
All_companies = All_companies[All_companies['AAOIFI_Compliant'] == True]

All_companies['Debt Ratio'] = All_companies['Total_Debt (M)'] / All_companies['Total_Assets (M)']

All_companies = All_companies.drop(columns=['Debt_Ratio'], errors='ignore') 

def Ev_ranking (row):
    Debt_uncertainty_rate = 'Great' if row['Debt Ratio'] <= 0.27 else( 'Average' if row['Debt Ratio'] <= 0.33 else 'Bad')
    return f'Debt ranking : {Debt_uncertainty_rate}'
All_companies['Ranking'] = All_companies.apply(Ev_ranking , axis= 1 )




All_companies = All_companies.sort_values(
    by=['Volatility (%)', 'ROE (%)', 'Dividend_Yield (%)'], 
    ascending=[True, False, False]
)

num_companies = len(All_companies)
ranks = list(range(num_companies, 0, -1)) 

All_companies['Portfolio_Weight (%)'] = [(r / sum(ranks)) * 100 for r in ranks]
All_companies['Portfolio_Weight (%)'] = All_companies['Portfolio_Weight (%)'].round(2)

print(All_companies[['Company Name', 'Volatility (%)', 'ROE (%)', 'Dividend_Yield (%)', 'Portfolio_Weight (%)']])



fig, axes = plt.subplots(2, 3, figsize=(15, 8)) 
fig.delaxes(axes.flat[-1])
metrics = ['Debt Ratio', 'ROE (%)', 'PE_Ratio', 'Dividend_Yield (%)', 'Portfolio_Weight (%)']
colors = ['brown', 'navy', 'orange', 'gold', 'green']

for ax, metric, color in zip(axes.flat, metrics, colors):
    ax.scatter(All_companies['Company Name'], All_companies[metric], color=color)
    ax.set_title(metric)
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('portfolio12_metrics.png', dpi=150)
plt.show()


All_companies.to_excel(r'C:\Users\Nisserine\Desktop\GOAL\Day 11\12\portfolio 12.xlsx' , 
                       engine='openpyxl')


