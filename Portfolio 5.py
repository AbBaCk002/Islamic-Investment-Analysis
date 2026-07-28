

# تحليل مبيعات شركة متكامل
# البيانات:

import pandas as pd 
import matplotlib.pyplot as plt 


data = {
    'employee_id': range(1, 13),
    'name': ['أحمد','سارة','خالد','نورة','فهد','منى',
             'عمر','ليلى','ياسر','هند','ماجد','ريم'],
    'department': ['مبيعات','مبيعات','تسويق','تسويق','مبيعات','مبيعات',
                   'تسويق','مبيعات','مبيعات','تسويق','مبيعات','مبيعات'],
    'region': ['شمال','جنوب','شمال','جنوب','شمال','جنوب',
               'شمال','جنوب','شمال','جنوب','شمال','جنوب'],
    'sales': [150000,230000,95000,88000,310000,120000,
              75000,195000,275000,60000,290000,145000],
    'costs': [45000,65000,30000,28000,85000,38000,
              25000,55000,78000,20000,82000,42000]
}

company = pd.DataFrame(data)
print(company)



company['profit'] = company['sales'] - company['costs']
company['profit_margin'] =(company['profit'] / company['sales']) * 100


print(company.nlargest(3, 'sales'))
print(company.groupby('department').agg({
    'sales' : ['sum' , 'mean' , 'count' ]
}))

company['pm_by_region'] = company.groupby('region')['profit_margin'].mean()

print("\n--- الموظفون الذين لديهم هامش ربح أقل من 25% ---")
print(company[company['profit_margin'] < 25.0][['name', 'profit_margin']]) # can pls tell me why do we use two brackets ? [[]]? 
# ====----
Desc = company.groupby('department')['sales'].sum().sort_values(ascending= False)
Desc.plot(kind='bar', color='grey', figsize=(10, 6))
plt.title('sales')
plt.xlabel('department')
plt.ylabel('sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('profit_analysis.png', dpi=150, bbox_inches='tight')  
plt.show()


Desc_r = company.groupby('region')['profit_margin'].mean().sort_values(ascending= False)
Desc_r.plot(kind='bar', color='grey', figsize=(10, 6))
plt.title(' profit_margin by region ')
plt.xlabel('department')
plt.ylabel('sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('profit_analysis.png', dpi=150, bbox_inches='tight')  
plt.show()


print(company)

print("=" * 50)
print("       تقرير تحليل المبيعات")
print("=" * 50)
print(f"Proft  : {company['profit']}")
print(f"profit_margin  : {company['profit_margin']}")  

print(f"top three employees : {company.nlargest(3, 'sales')}" )
print(f" sales by region : {company.groupby('department').agg({
    'sales' : ['sum' , 'mean' , 'count' ]
})}")
print("\n--- الموظفون الذين لديهم هامش ربح أقل من 25% ---")
print(company[company['profit_margin'] < 25.0][['name', 'profit_margin']])



print(f"profit_margin  : {company.groupby('region')['profit_margin'].mean()}")  


company.to_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Fifth\Real_Rpof_5.xlsx', engine= 'openpyxl'
)


 
