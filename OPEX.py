import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Импортируем df_income_sorted из вашего модуля Revenue
from Revenue import df_income_sorted

df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'], errors='coerce')
df_income_sorted['operatingExpenses'] = pd.to_numeric(df_income_sorted['operatingExpenses'], errors='coerce')

df_income_sorted = df_income_sorted.sort_values(by='fiscalDateEnding').reset_index(drop=True)

# Скользящее среднее за 3 года для сглаживания
df_income_sorted['OPEX_smooth'] = df_income_sorted['operatingExpenses'].rolling(window=3, min_periods=1).mean()

# Логарифмирование OPEX
y_log = np.log(df_income_sorted['OPEX_smooth'].values).reshape(-1, 1)
x_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

degree = 2
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(x_year)

model = LinearRegression()
model.fit(X_poly, y_log)

future_years = np.arange(2025, 2031).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly)

# Обратное преобразование
future_pred = np.exp(future_log_pred).flatten()

df_opex_forecast = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedOpex': future_pred
})

print(df_opex_forecast)