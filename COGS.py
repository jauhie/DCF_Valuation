import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from Revenue import df_income_sorted

# --- Подготовка данных ---
df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'], errors='coerce')
df_income_sorted['costofGoodsAndServicesSold'] = pd.to_numeric(df_income_sorted['costofGoodsAndServicesSold'], errors='coerce')

# Сортировка по дате
df_income_sorted = df_income_sorted.sort_values(by='fiscalDateEnding').reset_index(drop=True)

# Скользящее среднее за 3 года
df_income_sorted['COGS_smooth'] = df_income_sorted['costofGoodsAndServicesSold'].rolling(window=3, min_periods=1).mean()

# Логарифмирование
y_log = np.log(df_income_sorted['COGS_smooth'].values).reshape(-1, 1)
x_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

# Полиномиальная регрессия
degree = 2
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(x_year)

model = LinearRegression()
model.fit(X_poly, y_log)

future_years = np.array([2025,2026,2027,2028,2029,2030]).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly)

# Обратное преобразование
future_pred = np.exp(future_log_pred).flatten()

df_cogs_forecast = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedCOGS': future_pred})

print(df_cogs_forecast)

