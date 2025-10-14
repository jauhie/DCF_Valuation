from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


years = np.arange(2018, 2024)

np.random.seed(42)
total_revenue = np.linspace(100, 250, len(years)) + np.random.normal(0, 10, len(years))
cost_of_goods = total_revenue * np.random.uniform(0.55, 0.65, len(years))
operating_income = total_revenue * np.random.uniform(0.12, 0.18, len(years))
net_income = operating_income - np.random.uniform(5, 15, len(years))

df_fake = pd.DataFrame({
    'year': years,
    'totalRevenue': total_revenue.round(2),
    'costOfGoods': cost_of_goods.round(2),
    'operatingIncome': operating_income.round(2),
    'netIncome': net_income.round(2)
})

#print(df_fake)

x = np.array(df_fake['year']).reshape(-1, 1)
y = np.array(df_fake['totalRevenue']).reshape(-1, 1)
degree = 2

scaller = StandardScaler()
x_scalled = scaller.fit_transform(x) #--- скалируем

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(x_scalled)

model = LinearRegression()
model.fit(X_poly, y)

y_pred = model.predict(X_poly)
print(y_pred)




