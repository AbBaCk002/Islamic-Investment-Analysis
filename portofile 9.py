
import pandas as pd 
import matplotlib.pyplot as plt 

monthly_sales = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\portofile 9\monthly_sales_raw.xlsx',
    engine='openpyxl'
)


monthly_sales.columns = monthly_sales.columns.str.strip().str.title()
monthly_sales['Category'] = monthly_sales['Category'].str.strip().str.title()
monthly_sales['Region'] = monthly_sales['Region'].str.strip().str.title()

monthly_sales['Amount (Mad)']= monthly_sales['Amount (Mad)'].fillna(monthly_sales['Amount (Mad)'].mean()).round(0)
print(monthly_sales)

monthly_sales = monthly_sales.drop_duplicates(subset=['Sale_Id'] , keep = 'first')
monthly_sales= monthly_sales.set_index('Sale_Id')



monthly_sales['Month'] = monthly_sales['Sale Date'].dt.month
sales_by_month = monthly_sales.groupby('Month')['Amount (Mad)'].sum()
sales_by_month.plot( kind = 'bar' , color = 'teal' ,  figsize = (10 , 6))
plt.title('Monthly sales')
plt.xlabel('Months')
plt.ylabel('Amount (MAD)')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.savefig('Monthly_Sales.png', dpi=150)
plt.show()

monthly_sales.to_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\portofile 9\Monthly sales portfolio 9.xlsx' , 
    engine='openpyxl'
)