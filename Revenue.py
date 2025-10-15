import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def convert_json_to_dataframe(balance_path = 'BalanceStatements.json',
                              income_path = 'IncomeStatements.json'):
    with open(balance_path, 'r') as f:
        balance_data = json.load(f)
    with open(income_path, 'r') as f:
        income_data = json.load(f)
    df_balance = pd.DataFrame(balance_data['annualReports'])
    df_income = pd.DataFrame(income_data['annualReports'])
    return df_balance, df_income

df_balance, df_income = convert_json_to_dataframe()                     #--- Dataframe хранится в переменных---

df_income_sorted = df_income.sort_values(by='fiscalDateEnding', ascending=True).reset_index(drop=True)
df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'], errors='coerce')
df_income_sorted['totalRevenue'] = pd.to_numeric(df_income_sorted['totalRevenue'], errors='coerce')

df_income_sorted = df_income_sorted.dropna(subset=['fiscalDateEnding', 'totalRevenue']).reset_index(drop=True)

# --- Сглаживание: скользящее среднее по 3 годам ---
df_income_sorted['Revenue_smooth'] = df_income_sorted['totalRevenue'].rolling(window=3, min_periods=1).mean()

# (Добавляем небольшую epsilon на случай нулевых значений)
epsilon = 1e-6
y_log = np.log(df_income_sorted['Revenue_smooth'].astype(float).values + epsilon).reshape(-1, 1)

X_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

degree = 2
poly = PolynomialFeatures(degree=degree, include_bias=False)
X_poly = poly.fit_transform(X_year)

model = LinearRegression()
model.fit(X_poly, y_log)

future_years = np.array([2025, 2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly)

future_revenue_pred = np.exp(future_log_pred).flatten()

future_revenue_pred = np.maximum(future_revenue_pred, 0.0)

df_revenue_pred = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedRevenue': future_revenue_pred
})

print(df_revenue_pred)