import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from OPEX import df_income_sorted


capex = np.array([{'2019':56565000,'2020':141737000, '2021':281598000,
          '2022':206165000, '2023':69045000, '2024':41195000}])

df_capex = pd.DataFrame(list(capex[0].items()), columns=['Year', 'Capex'])

df_capex['SmootedCAPEX'] =df_capex['Capex'].rolling(window=3, min_periods=1).mean()

x_log = np.log(df_capex['SmootedCAPEX'].values).reshape(-1, 1)
y_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

degree = 1
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(y_year)

model = LinearRegression()
model.fit(X_poly, x_log)

#print(f"R² score CAPEX: {model.score(X_poly, x_log):.4f}")
future_years = np.arange(2025, 2031).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly)
future_pred = np.exp(future_log_pred).flatten()

df_capex_forecast = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedCapex': future_pred})
