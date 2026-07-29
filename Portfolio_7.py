
import pandas as pd
import matplotlib.pyplot as plt 
customers = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portofoio_7\customers_raw.xlsx', engine= 'openpyxl'
)

orders = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portofoio_7\orders_raw.xlsx', engine= 'openpyxl'

)

customers.columns = customers.columns.str.strip().str.title()
orders.columns = orders.columns.str.strip().str.title()

customers['City'] = customers['City'].str.strip().str.capitalize()
customers['Membership Tier'] = customers['Membership Tier'].str.strip().str.capitalize()

customers['Signup Date'] = pd.to_datetime(customers['Signup Date'], errors='coerce') #
customers['Signup Date']= customers['Signup Date'].fillna('Unkown date')
customers['Customer Name'] = customers['Customer Name'].fillna('Unknown Name ')
customers= customers.drop_duplicates(subset=['Customer Name'] , keep= 'first') 


orders['Data_Issue'] = 'Valid'

orders.loc[orders['Cust_Id'].isin([999, 998]), 'Data_Issue'] = 'Orphan Customer ID (Unmapped)'

orders['Net Amount'] = orders['Order Amount'] * (1 - orders['Discount %'] /100) 
full = pd.merge(customers , orders , on= 'Cust_Id' ,how= 'right')
full= full.set_index('Cust_Id')

dept_pivot = full.pivot_table(
    index='City',
    columns='Membership Tier',
    values='Net Amount', 
    aggfunc='mean' 
)
dept_pivot = dept_pivot


print(
full.groupby('Membership Tier').agg({ 
    'Net Amount' : ['sum', 'count', 'mean']
}))

print(full)


plt.figure(figsize=(10, 5))
plt.bar(full['Customer Name'], full['Order Amount'], color='teal')
plt.title('إجمالي المبيعات لكل موظف (Total Sales per Employee)')
plt.xlabel('الموظف')
plt.ylabel('المبيعات (MAD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('customer_orders.png', dpi=150)
plt.show()


ax = dept_pivot.plot(kind='bar',color='darkorange', figsize=(10, 6))
plt.title('متوسط المبيعات حسب  (Average Sales by Membership Tier)')
plt.xlabel('Membership Tier')
plt.ylabel('متوسط المبيعات (MAD)')
plt.tight_layout()
plt.savefig('Membership Tier_average.png', dpi=150)
plt.show()

full.to_excel(
        r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\Portfolio_7.xlsx', engine= 'openpyxl'
)

