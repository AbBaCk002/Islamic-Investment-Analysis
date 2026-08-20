
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


# Order_Amount_Average = full['Order Amount'].mean()
# full['Order Amount'] = full['Order Amount'].fillna(Order_Amount_Average).round(0)

orders['Net Amount'] = orders['Order Amount'] * (1 - orders['Discount %'] /100) 
full = pd.merge(customers , orders , on= 'Cust_Id' ,how= 'right')
full= full.set_index('Cust_Id')

# fillna(0) instead of mean: Orphan IDs (999, 998) have unconfirmed values.
# Replacing with 0 avoids inflating total sales without empirical proof.
full['Order Amount'] = full['Order Amount'].fillna(0)
full['Net Amount'] = full['Net Amount'].fillna(0)


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
valid_customers = full.dropna(subset=['Customer Name'])

plt.figure(figsize=(10, 5))
plt.bar(valid_customers['Customer Name'], valid_customers['Order Amount'], color='teal')
plt.title('Total Sales per Customer')
plt.xlabel('Customer')
plt.ylabel('Sales (MAD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('customer_orders.png', dpi=150)
plt.show()

colors = ['#cd7f32', '#ffd700', '#c0c0c0']  # برونزي، ذهبي، فضي
ax = dept_pivot.plot(kind='bar',color = colors,  figsize=(10, 6))
plt.title('Average Sales by Membership Tier')
plt.xlabel('Membership Tier')
plt.ylabel('Average sales(MAD)')
plt.tight_layout()
plt.savefig('Membership Tier_average.png', dpi=150)
plt.show()

full.to_excel(
        r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\Portfolio_7.xlsx', engine= 'openpyxl'
)

