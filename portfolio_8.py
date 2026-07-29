
import pandas as pd 
import matplotlib.pyplot as plt 

customers = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portfolio_8\customers_raw.xlsx' , 
    engine='openpyxl'
)
orders = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portfolio_8\orders_raw.xlsx' , 
    engine='openpyxl'
)
products = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portfolio_8\products_raw.xlsx' ,
    engine='openpyxl'
)


customers.columns = customers.columns.str.strip().str.title()
orders.columns = orders.columns.str.strip().str.title()
products.columns = products.columns.str.strip().str.title()

customers['City'] = customers['City'].str.strip().str.capitalize()
customers['Membership Tier'] = customers['Membership Tier'].str.strip().str.capitalize()
customers['Customere Name'] = customers['Customer Name'].str.strip().str.title()
customers['Customer Name']= customers['Customer Name'].fillna('Unknown Name')
products['Category'] = products['Category'].str.strip().str.capitalize()
orders['Order Date'] = pd.to_datetime(orders['Order Date'] , errors= 'coerce')

orders['Data_Issue'] = 'Valid'

orders.loc[orders['Cust_Id'].isin([401, 402]), 'Data_Issue'] = 'Orphan Customer ID'
orders.loc[orders['Product_Id'] == 'P99', 'Data_Issue'] = 'Unmapped Product (P99)'

products = products.drop_duplicates(subset=['Product_Id'], keep='first')
products['Unit Price'] = products['Unit Price'].fillna(products['Unit Price'].mean())

full = pd.merge (customers , orders , on= 'Cust_Id' ,  how='right' )
full = pd.merge(full  , products , on = 'Product_Id' , how= 'left')


full['Total'] = full['Quantity'] * full['Unit Price']


def eve(row):
    if pd.isna(row['Total']):
        return 'Unknown'
    return 'Large' if row['Total'] > 500 else 'Small'

full['Ranking'] = full.apply(eve , axis =1)


print(full.groupby(['City' , 'Category']).agg({
    'Total' : 'sum'
}))


customer_sales = full.groupby('Customer Name')['Total'].sum().dropna().reset_index()
plt.figure(figsize=(10, 5))
plt.bar(customer_sales['Customer Name'], customer_sales['Total'], color='teal')
plt.title('إجمالي المبيعات لكل موظف (Total Sales per Customer)')
plt.xlabel('Customer')
plt.ylabel('المبيعات (MAD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Customer_sales.png', dpi=150)
plt.show()


city_sales = full.groupby('City')['Total'].sum().dropna().reset_index()
plt.figure(figsize=(8, 5))
plt.bar(city_sales['City'], city_sales['Total'], color='darkorange')
plt.title('(Sales by City')
plt.xlabel('Department')
plt.ylabel(' المبيعات (MAD)')
plt.tight_layout()
plt.savefig('City_Sales.png', dpi=150)
plt.show()


full.to_excel (
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\files_portfolio_8\porfolio 8.xlsx' ,
    engine='openpyxl'
)

