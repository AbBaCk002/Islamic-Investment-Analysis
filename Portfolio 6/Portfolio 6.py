



import pandas as pd 
import matplotlib.pyplot as plt 

employees = pd.read_excel (
        r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\portfolio 6 excell\employees_raw.xlsx',
        engine= 'openpyxl'
)

sales = pd.read_excel(
    r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\portfolio 6 excell\sales_raw.xlsx',
    engine='openpyxl'
)

employees.columns = employees.columns.str.upper().str.strip()
sales.columns = sales.columns.str.upper().str.strip()

employees['EMP_ID'] = employees['EMP_ID'].astype(str).str.strip()
employees['EMP_ID'] = pd.to_numeric(employees['EMP_ID'], errors='coerce')

employees= employees.drop_duplicates(subset=['EMP_ID'] , keep= 'first')
employees['REGION'] = employees['REGION'].str.upper().str.strip()
employees['DEPARTMENT'] = employees['DEPARTMENT'].str.upper().str.strip()
employees['HIRE DATE'] = pd.to_datetime(employees['HIRE DATE'], errors='coerce') 
employees['FULL NAME'] = employees['FULL NAME'].fillna('Unknown Name (106)')
average_salary = employees['MONTHLY SALARY (MAD)'].mean()
employees['MONTHLY SALARY (MAD)'] = employees['MONTHLY SALARY (MAD)'].fillna(average_salary).round(0) 
employees['HIRE DATE'] = employees['HIRE DATE'].ffill() 
#--

sales['SALE AMOUNT'] = sales['SALE AMOUNT'].astype(str).str.strip() 
sales['SALE AMOUNT'] = pd.to_numeric(sales['SALE AMOUNT'], errors='coerce')
sales['EMPLOYEE_ID'] = sales['EMPLOYEE_ID'].replace(999, 106)
average_sales = sales['SALE AMOUNT'].mean()
sales['SALE AMOUNT'] = sales['SALE AMOUNT'].fillna(average_sales).round(0)
sales['SALE AMOUNT'] = pd.to_numeric(sales['SALE AMOUNT'], errors='coerce')

sales['SALE_DATE'] = sales['SALE_DATE'].astype(str).str.strip() 
sales['SALE_DATE'] = sales['SALE_DATE'].str.upper().str.strip()
sales['SALE_DATE'] = pd.to_datetime(sales['SALE_DATE'])

final_table = pd.merge(sales, employees, left_on='EMPLOYEE_ID', right_on='EMP_ID', how='left')
employee_sales = final_table.groupby('FULL NAME')['SALE AMOUNT'].sum().sort_values(ascending=False).reset_index()


# print(final_table[final_table['EMPLOYEE_ID'] == 106][['EMPLOYEE_ID', 'FULL NAME', 'SALE AMOUNT', 'SALE_DATE']])
final_table['PROFIT'] = final_table['SALE AMOUNT'] - final_table['COST'] 

final_table = final_table.set_index('EMPLOYEE_ID')

dept_pivot = final_table.pivot_table(
    values='SALE AMOUNT', 
    index='DEPARTMENT', 
    aggfunc='mean' 
)

dept_pivot.columns = ['Average_Sales']
# print(dept_pivot)

dept_pivot = dept_pivot.reset_index()


plt.figure(figsize=(10, 5))
plt.bar(employee_sales['FULL NAME'], employee_sales['SALE AMOUNT'], color='teal')
plt.title('Total Sales per Employee')
plt.xlabel('Employee')
plt.ylabel('Sales (MAD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Total Sales per Employee.png', dpi=150)
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(dept_pivot['DEPARTMENT'], dept_pivot['Average_Sales'], color='darkorange')
plt.title('Average Sales by Department')
plt.xlabel('Department')
plt.ylabel('Average Sales (MAD)')
plt.tight_layout()
plt.savefig('Average Sales by Department.png', dpi=150)
plt.show()


final_table.to_excel(
        r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Portfolio 6\portfolio 6 excell\Portfolio_6.xlsx', engine= 'openpyxl'
)
