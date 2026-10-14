import pandas as pd 
import matplotlib.pyplot as plt 
import os
import streamlit  as st 

dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, 'companies_financials_raw.xlsx')
banks = pd.read_excel(file_path, engine='openpyxl')


banks['Sector'] = banks['Sector'].str.strip().str.title()
average = banks['Total_Debt (M)'].mean()
banks['Total_Debt (M)'] = banks['Total_Debt (M)'].fillna(average).round(0)

banks['Debt_Ratio'] = banks['Total_Debt (M)'] / banks['Total_Assets (M)'] 
banks['Haram_Income_Ratio'] = banks['Interest_Income (M)'] / banks['Total_Revenue (M)'] 
banks['Liquidity_Ratio'] = banks['Cash_and_Liquid_Assets (M)'] / banks['Total_Assets (M)']
banks = banks.drop_duplicates(subset=['Company Name'], keep='first')
banks.columns = banks.columns.str.strip()

def Ev_ranking (row):
    Debt_ranking = 'Great' if row['Debt_Ratio'] <= 0.32 else 'Bad'
    R_Haram_Income_Ratio = 'Great' if row['Haram_Income_Ratio'] <=0.04 else 'Bad' 
    R_Liquidity_Ratio =  'Bad' if row ['Liquidity_Ratio'] <= 0.51 else 'Great'
    return f'Debt_ranking : {Debt_ranking} | Haram_Income_Ratio : {R_Haram_Income_Ratio} | Liquidity_Ratio :  {R_Liquidity_Ratio} ' 
banks['Ranking'] = banks.apply(Ev_ranking , axis= 1 )

def Ranking_By_Points(row):
    score  = 0 
    if row['Debt_Ratio'] >= 0.33 : score += 1 
    if row ['Haram_Income_Ratio']  >= 0.05 : score += 1 
    if row ['Liquidity_Ratio'] <= 0.51 : score += 1
    return f'Ranking_By_Points : {score}/3'
banks['P_Ranking'] = banks.apply(Ranking_By_Points , axis= 1 )
def check_business(sector):
    unhalal_sectors = ['Alcohol', 'Gambling', 'Banking']
    if sector in unhalal_sectors:
        return 'No'
    else:
        return 'Yes'
banks['Halal_Business'] = banks['Sector'].apply(check_business)


def aaoifi(row):
    if (row['Halal_Business'] == 'Yes' and 
        row['Debt_Ratio'] < 0.33 and 
        row['Haram_Income_Ratio'] < 0.05 and 
        row['Liquidity_Ratio'] > 0.51):
        return True
    else:
        return False
banks['AAOIFI_Compliant'] = banks.apply(aaoifi, axis=1)
banks= banks.set_index('Company_ID')

plt.figure(figsize=(10, 6))
plt.scatter(banks['P_Ranking'], banks['Company Name'], alpha=0.7, edgecolors='black')
plt.title('Ranking by Points')
plt.xlabel('P Raning ')
plt.ylabel('Company Name ')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Ranking By Points_Compamies', dpi=150)

plt.show()


plt.figure(figsize=(10, 6))
plt.scatter( banks['P_Ranking'],banks['Sector'], alpha=0.7, edgecolors='black')
plt.title('Ranking by Points')
plt.xlabel('P Raning ')
plt.ylabel('Sector')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Ranking By Points_Sector.png', dpi=150)

plt.show()

# --- عرض الرسم البياني الأول ---
st.subheader("📊 Ranking by Points per Company")
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(
    banks["P_Ranking"], banks["Company Name"], alpha=0.7, edgecolors="black"
)
ax1.set_title("Ranking by Points")
ax1.set_xlabel("P Ranking")
ax1.set_ylabel("Company Name")
ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)  # <-- عرض الرسم البياني على صفحة Streamlit

# --- عرض الرسم البياني الثاني ---
st.subheader("📊 Ranking by Points per Sector")
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.scatter(banks["P_Ranking"], banks["Sector"], alpha=0.7, edgecolors="black")
ax2.set_title("Ranking by Points")
ax2.set_xlabel("P Ranking")
ax2.set_ylabel("Sector")
ax2.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig2)  # <-- عرض الرسم البياني الثاني على الصفحة

# --- عرض الجدول النهائي للبيانات ---
st.subheader("📋 Filtered Banks & Financial Data")
st.dataframe(banks.reset_index())




output_path = os.path.join(dir, "Re_portfolio_11.xlsx")
banks.reset_index().to_excel(output_path, index=False, engine="openpyxl")






