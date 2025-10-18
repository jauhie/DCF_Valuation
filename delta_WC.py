import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from Revenue import df_balance

#--- Импорт данных и их подготовка
df_balance_sorted = df_balance.sort_values(by='fiscalDateEnding', ascending=True).reset_index(drop=True)
df_balance_sorted['fiscalDateEnding'] = pd.to_datetime(df_balance_sorted['fiscalDateEnding'],
                                                       errors='coerce')
df_balance_sorted['totalAssets'] = pd.to_numeric(df_balance_sorted['totalAssets'], errors='coerce')
df_balance_sorted['totalLiabilities'] = pd.to_numeric(df_balance_sorted['totalLiabilities'],
                                                      errors='coerce')

df_balance_sorted['WorkingCapital'] = (df_balance_sorted['totalAssets']
                                       - df_balance_sorted['totalLiabilities'])

df_wc = pd.concat([df_balance_sorted['fiscalDateEnding'],
                   df_balance_sorted['totalAssets'],
                   df_balance_sorted['totalLiabilities'],
                   df_balance_sorted['WorkingCapital']], axis=1)

#--- Сглаживание значений WC
df_wc['SmootedWC'] =df_wc['WorkingCapital'].rolling(window=3, min_periods=1).mean()

y_year = df_balance_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)
x_wc = np.log(df_wc['SmootedWC'].values).reshape(-1, 1)

if np.isnan(x_wc).any() or np.isnan(y_year).any():
    print("ВНИМАНИЕ: Есть пропущенные значения в данных!")
    #---Заполним пропущенные значения
    x_wc = np.nan_to_num(x_wc)
    y_year = np.nan_to_num(y_year)

degree = 2
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(y_year)

model = LinearRegression()
model.fit(X_poly,x_wc)

#print(f"R² score delta_WC: {model.score(X_poly, x_wc):.4f}")

future_years = np.arange(2025, 2031).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly).flatten()

future_pred = np.exp(future_log_pred)

max_historical = df_wc['WorkingCapital'].max() * 2.0  # Увеличиваем до 200%
min_historical = df_wc['WorkingCapital'].min() * 0.5  # Уменьшаем до 50%
future_pred = np.clip(future_pred, min_historical, max_historical)

df_wc_forecast = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedWC': future_pred})


