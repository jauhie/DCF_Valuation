import json
import numpy as np
import pandas as pd
from pandas import DataFrame
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
df_balance_sorted = df_balance.sort_values(by='fiscalDateEnding', ascending=True).reset_index(drop=True)

df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'],
                                               errors='coerce')
x = np.array(df_income_sorted['fiscalDateEnding'].dt.year).reshape(-1, 1)      #--- dt.year извлекает из данных только год---
y = np.array(df_income_sorted['totalRevenue']).reshape(-1, 1)
degree = 2

scaller = StandardScaler()
x_scalled = scaller.fit_transform(x)

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(x_scalled)

model = LinearRegression()
model.fit(X_poly, y)
future_years = np.array([2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]).reshape(-1, 1)
future_years_scaller = scaller.transform(future_years)
future_poly = poly.transform(future_years_scaller)

future_pred = model.predict(future_poly).flatten()

df_test = pd.DataFrame({'Years': np.ravel(future_years), 'PredictedRevenue': np.ravel(future_pred)})
print(df_test)
print(df_income_sorted)