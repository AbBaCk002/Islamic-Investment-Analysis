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
All_companies = All_companies[All_companies['AAOIFI_Compliant'] == True] # how is that works ? , cuz we don't set anything ! 

All_companies['Debt Ratio'] = All_companies['Total_Debt (M)'] / All_companies['Total_Assets (M)']

All_companies = All_companies.drop(columns=['Debt_Ratio'], errors='ignore') # remove the firts culome to keep one ! 

def Ev_ranking (row):
    Debt_uncertainty_rate = 'Great' if row['Debt Ratio'] <= 0.27 else( 'Average' if row['Debt Ratio'] <= 0.33 else 'Bad')
    return f'Debt ranking : {Debt_uncertainty_rate}'
All_companies['Ranking'] = All_companies.apply(Ev_ranking , axis= 1 )





# 1. الترتيب حسب الشروط الثلاثة معاً (الاستقرار أولاً ثم الربحية)
# Volatility تصاعدي (True) | ROE تنازلي (False) | Dividend_Yield تنازلي (False)
All_companies = All_companies.sort_values(
    by=['Volatility (%)', 'ROE (%)', 'Dividend_Yield (%)'], 
    ascending=[True, False, False]
)

# 2. إعطاء نقاط/ترتيب لكل شركة (الشركة الأولى الأفضل تأخذ أعلى نقاط)
num_companies = len(All_companies)
ranks = list(range(num_companies, 0, -1)) # مثلاً من 10 إلى 1

# 3. حساب الوزن المئوي لكل شركة (مجموع الأوزان سيكون 100%)
# المنطق: وزن الشركة = (نقاط الشركة / مجموع نقاط كل الشركات) * 100
All_companies['Portfolio_Weight (%)'] = [(r / sum(ranks)) * 100 for r in ranks]
All_companies['Portfolio_Weight (%)'] = All_companies['Portfolio_Weight (%)'].round(2)

# عرض النتيجة للتأكد
print(All_companies[['Company Name', 'Volatility (%)', 'ROE (%)', 'Dividend_Yield (%)', 'Portfolio_Weight (%)']])



# not working ----------------------------------------------
# All_companies = All_companies.set_index('Company_ID')
# # print(All_companies)
# # Scompany = All_companies.groupby('Sector')[['Company Name', 'Volatility (%)', 'ROE (%)', 'Dividend_Yield (%)', 'Portfolio_Weight (%)']]
# plt.figure(figsize=(10, 6))
# plt.scatter( All_companies['Company Name'],All_companies['Debt Ratio'] ,color='brown', alpha=0.7, edgecolors='black', label = 'Debt Ratio' , marker = 's')
# plt.scatter( All_companies['Company Name'],All_companies['ROE (%)'] ,color='navy', alpha=0.7, edgecolors='black', label = 'ROE (%)' , marker = 's')
# plt.scatter( All_companies['Company Name'],All_companies['PE_Ratio'] ,color='Orange', alpha=0.7, edgecolors='black', label = 'PE_Ratio' , marker = 's')
# plt.scatter( All_companies['Company Name'],All_companies['Dividend_Yield (%)'] ,color='yellow', alpha=0.7, edgecolors='black', label = 'Dividend_Yield (%)' , marker = 's')
# plt.scatter( All_companies['Company Name'],All_companies['Portfolio_Weight (%)'] ,color='Green', alpha=0.7, edgecolors='black', label = 'Portfolio_Weight (%)' , marker = 's')

# plt.title('Companies Statistics')
# plt.xlabel('Company Name ')
# plt.ylabel('Statistics' )
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.tight_layout()
# plt.show()



# i don't like this one ! 
# plt.plot(All_companies['Company Name'] ,  All_companies['PE_Ratio'] , label = 'Volatility (%)' , marker = 'o')
# plt.plot(All_companies['Company Name'] ,  All_companies['ROE (%)'] , label = 'Volatility (%)' , marker = 'o')
# plt.plot(All_companies['Company Name'] , All_companies['Dividend_Yield (%)'] , label = 'Dividend_Yield (%)' , marker = 'o')
# plt.plot(All_companies['Company Name'] ,  All_companies['Volatility (%)'] , label = 'Volatility (%)' , marker = 'o')
# # plt.plot(second['quarter'] , second['product_C'] , label = 'C' , marker = '^')
# plt.title('Companies')
# plt.xlabel('Companies name')
# plt.ylabel('Percentage % ')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.legend()
# plt.show()

# not working --------------------------------------------------------------




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
# All_companies.to_excel(r'C:\Users\Nisserine\Desktop\GOAL\Day 11\12\portfolio 12.xlsx' , 
#                        engine='openpyxl')


