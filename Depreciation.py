import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from CAPEX import df_capex, df_capex_forecast
from OPEX import df_income_sorted

df_income_sorted['fiscalDateEnding'] = pd.to_datetime(df_income_sorted['fiscalDateEnding'], errors='coerce')
df_income_sorted['depreciationAndAmortization'] = pd.to_numeric(df_income_sorted['depreciationAndAmortization'],
                                                                errors='coerce')

df_income_sorted = df_income_sorted.sort_values(by='fiscalDateEnding').reset_index(drop=True)

df_income_sorted['depreciation_smooth'] = df_income_sorted['depreciationAndAmortization'].rolling(window=3, min_periods=1).mean()

y_log = np.log(df_income_sorted['depreciation_smooth'].values).reshape(-1, 1)
x_year = df_income_sorted['fiscalDateEnding'].dt.year.values.reshape(-1, 1)

degree = 2
poly = PolynomialFeatures(degree=degree)
X_poly = poly.fit_transform(x_year)

model = LinearRegression()
model.fit(X_poly, y_log)

#print(f"R² score depreciation: {model.score(X_poly, y_log):.4f}")

future_years = np.arange(2025, 2031).reshape(-1, 1)
future_poly = poly.transform(future_years)
future_log_pred = model.predict(future_poly)
future_pred = np.exp(future_log_pred).flatten()

conservative_pred = [future_pred[0]]  # Начинаем с первого прогнозного значения

for i in range(1, len(future_pred)):
    max_growth = 0.08  # Снизили до 8% в год
    next_value = min(future_pred[i], conservative_pred[i-1] * (1 + max_growth))
    conservative_pred.append(next_value)

df_depreciation_forecast = pd.DataFrame({
    'Year': future_years.flatten(),
    'PredictedDepreciation': future_pred,
    'PredictedDepreciation_Conservative': conservative_pred
})

#print("Оригинальный прогноз:")
#print(df_depreciation_forecast['PredictedDepreciation'])
#print("\nКонсервативный прогноз (макс. рост 8% в год):")
#print(df_depreciation_forecast['PredictedDepreciation_Conservative'])

# Расчет темпов роста
growth_rates = df_depreciation_forecast['PredictedDepreciation_Conservative'].pct_change().dropna()
#print(f"\nСреднегодовой рост консервативного прогноза: {growth_rates.mean():.1%}")




