import sqlite3 
import pandas as pd 
import matplotlib.pyplot as plt 

Scompany = sqlite3.connect(r'C:\Users\Nisserine\Desktop\GOAL\Day 11\14\retail_analytics.db')

first_query = """
WITH monthly_revenue AS (
    SELECT 
        STRFTIME('%Y-%m', o1.order_date) AS month,
        SUM(oi1.quantity * p1.unit_price) AS total_revenue
    FROM orders o1
    JOIN order_items oi1 ON o1.order_id = oi1.order_id
    JOIN products p1 ON oi1.product_id = p1.product_id 
    GROUP BY STRFTIME('%Y-%m', o1.order_date)
),
monthly_changes AS (
    SELECT 
        month,
        total_revenue,
        LAG(total_revenue) OVER (ORDER BY month) AS previous_month_revenue,
        total_revenue - LAG(total_revenue) OVER (ORDER BY month) AS revenue_change
    FROM monthly_revenue
)
SELECT * 
FROM monthly_changes 
ORDER BY month;
"""

first_company = pd.read_sql_query(first_query, Scompany)

# ==============

second_query = """
with first as (
	SELECT c1.customer_id , c1.customer_name ,sum(oi1.quantity * p1.unit_price) as expenses
  	FROM customers c1 
  	LEFT JOIN orders o1 on c1.customer_id = o1.customer_id
  	left JOIN order_items oi1 on o1.order_id = oi1.order_id
  	left JOIN products p1 on oi1.product_id = p1.product_id
  GROUP by c1.customer_id , c1.customer_name
),
second as (
	SELECT customer_id , customer_name ,expenses ,
  	RANK() OVER(order by expenses  DESC) as Best_10
  	FROM first
),
third as (
	SELECT customer_id , customer_name ,expenses , Best_10
  	FROM second
)
SELECT * FROM third  
WHERE Best_10 <= 10;
"""

second_company = pd.read_sql_query(second_query , Scompany)



third_query = """
with first as (
	SELECT p1.category, c1.city ,sum(oi1.quantity * p1.unit_price) as expenses
  	FROM customers c1 
  	LEFT JOIN orders o1 on c1.customer_id = o1.customer_id
  	left JOIN order_items oi1 on o1.order_id = oi1.order_id
  	left JOIN products p1 on oi1.product_id = p1.product_id
  GROUP by p1.category ,c1.city
),
second as (
	SELECT category , city ,expenses ,
  	RANK() OVER(PARTITION by city   order by expenses  DESC) as ranking
  	FROM first
),
third as (
	SELECT category , city ,expenses , ranking
  	FROM second
)
SELECT * FROM third  
where ranking = 1 ;
"""
third_company = pd.read_sql_query(third_query , Scompany)



fourth_query = """
with first as (
	SELECT 
    c1.customer_id,
    c1.customer_name,
    MAX(o1.order_date) AS last_order_date,
    CAST(
        JULIANDAY((SELECT MAX(order_date) FROM orders)) - JULIANDAY(MAX(o1.order_date)) 
    AS INTEGER) AS days_ago  
FROM customers c1
LEFT JOIN orders o1 ON c1.customer_id = o1.customer_id
GROUP BY c1.customer_id, c1.customer_name
HAVING days_ago > 90
),
second as (
	SELECT customer_id, customer_name, last_order_date , days_ago ,
  	  	RANK() OVER (ORDER BY days_ago DESC) as rank 
 	 FROM first 
),
third as (
	SELECT customer_id, customer_name, last_order_date , days_ago ,rank 
 	 FROM second 
)
SELECT * FROM third 
"""

fourth_company = pd.read_sql_query (fourth_query , Scompany)

colors = ['#cd7f32', '#ffd700', '#c0c0c0'] 
first_company.plot( kind = 'line' , color = colors , x='month', y='total_revenue', marker='o', figsize = (10 , 6))
plt.title('monthly_revenue')
plt.xlabel('Months')
plt.ylabel('revenue')
plt.tight_layout()
plt.grid(True)              
plt.savefig('monthly_revenue.png', dpi=150)
plt.show()
#--
second_company.plot( kind = 'bar' , color = '#c0c0c0', x='customer_name', y='expenses', figsize = (10 , 6))
plt.title('Best 10 Customers by expenses')
plt.xlabel('customers')
plt.ylabel('expenses')
plt.tight_layout()
plt.grid(True)              
plt.savefig('Best 10.png', dpi=150)
plt.show()


third_company['city_category'] = third_company['city'] + ' - ' + third_company['category']
third_company.plot( kind='bar', x='city_category', y='expenses',color='#cd7f32', figsize=(10, 6))
plt.title('Top Selling Category per City')
plt.xlabel('City & Category')     
plt.ylabel('Expenses')   
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.savefig('Revenue_by_City_and_Category.png', dpi=150)
plt.show()



fourth_company.plot(kind= 'bar' ,x= 'customer_name' , y = 'days_ago' , color ='silver' , figsize =(10 ,6))
plt.title('Absent customers over 90 days')
plt.xlabel('Customer name')
plt.ylabel('Days Inactive')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.savefig('Absent customers.png' , dpi= 150)
plt.show()


full = """
SELECT * 
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN products ON order_items.product_id = products.product_id
"""

all_tables = pd.read_sql_query(full, Scompany)

with pd.ExcelWriter(r'C:\Users\Nisserine\Desktop\GOAL\Day 11\14\Retail_Analytics_Final.xlsx', engine='openpyxl') as writer:
    all_tables.to_excel(writer, sheet_name='All tables', index=False)
    
    first_company.to_excel(writer, sheet_name='Monthly Sales', index=False)
    second_company.to_excel(writer, sheet_name='Top Customers', index=False)
    third_company.to_excel(writer, sheet_name='Revenue City Category', index=False)
    fourth_company.to_excel(writer, sheet_name='Absent Customers', index=False)

