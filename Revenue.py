import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def convert_json_to_dataframe(balance_path='BalanceStatements.json',
                              income_path='IncomeStatements.json'):
    with open(balance_path, 'r') as f:
        balance_data = json.load(f)
    with open(income_path, 'r') as f:
        income_data = json.load(f)
    df_balance = pd.DataFrame(balance_data['annualReports'])
    df_income = pd.DataFrame(income_data['annualReports'])
    return df_balance, df_income

df_balance, df_income = convert_json_to_dataframe()

df_income_sorted = df_income.sort_values(by='fiscalDateEnding', ascending=True).reset_index(drop=True)
df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'], errors='coerce')
df_income_sorted['totalRevenue'] = pd.to_numeric(df_income_sorted['totalRevenue'], errors='coerce')

df_income_sorted = df_income_sorted.dropna(subset=['fiscalDateEnding', 'totalRevenue']).reset_index(drop=True)

# --- Сглаживание: скользящее среднее по 3 годам ---
df_income_sorted['Revenue_smooth'] = df_income_sorted['totalRevenue'].rolling(window=3, min_periods=1).mean()

y = df_income_sorted['Revenue_smooth'].values.reshape(-1, 1)  # Без np.log()

X_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

#---Простая линейная регрессия вместо полиномиальной
model = LinearRegression()
model.fit(X_year, y)

print(f"R² score Revenue: {model.score(X_year, y):.4f}")
print(f"Коэффициент (годовой рост): {model.coef_[0][0]:.0f}")  # Показывает $ роста в год

future_years = np.array([2025, 2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)

future_revenue_pred = model.predict(future_years).flatten()

#---прогноз не должен быть ниже последнего исторического значения
last_historical_revenue = df_income_sorted['Revenue_smooth'].iloc[-1]
future_revenue_pred = np.maximum(future_revenue_pred, last_historical_revenue)

df_revenue_pred = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedRevenue': future_revenue_pred})

print("Историческая выручка:")
print(df_income_sorted['totalRevenue'])
print("\nПрогноз выручки:")
print(df_revenue_pred)