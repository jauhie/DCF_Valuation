import numpy as np
import pandas as pd
from CAPEX import df_capex_forecast
from Depreciation import df_depreciation_forecast
from EBIT import df
from WACC import TaxRate_sweden
from delta_WC import df_wc_forecast

#---FCF = EBIT*(1 - Tax) + Dep - CAPEX - ΔWC

future_years = np.arange(2025, 2031)
df_fcf = pd.DataFrame({'Year': future_years})

min_length = min(len(df), len(df_capex_forecast),
                len(df_depreciation_forecast), len(df_wc_forecast))

# Обрезаем данные до минимальной длины
years = future_years[:min_length]
df_fcf = pd.DataFrame({'Year': years})

df_fcf['EBIT'] = df['ForecastEBIT'].values[:min_length] if 'ForecastEBIT' in df else 0
df_fcf['Depreciation'] = df_depreciation_forecast['PredictedDepreciation_Conservative'].values[:min_length]
df_fcf['CAPEX'] = df_capex_forecast['PredictedCapex'].values[:min_length]
df_fcf['Delta_WC'] = df_wc_forecast['PredictedWC'].values[:min_length]

df_fcf['EBIT_after_tax'] = df_fcf['EBIT'].apply(lambda x: x * (1 - TaxRate_sweden) if x > 0 else x)

df_fcf['ForecastFCF'] = (df_fcf['EBIT_after_tax'] +
                         df_fcf['Depreciation'] -
                         df_fcf['CAPEX'] -
                         df_fcf['Delta_WC'])

#print("\n=== ПРОГНОЗ FCF ===")
#print(df_fcf)

# Детализированный вывод
#print("\n=== ДЕТАЛИЗАЦИЯ РАСЧЕТА FCF ===")
#for i, row in df_fcf.iterrows():
#    print(f"\n{row['Year']}:")
#    print(f"  EBIT: {row['EBIT']:,.0f}")
#    print(f"  EBIT после налога ({TaxRate_sweden:.1%}): {row['EBIT_after_tax']:,.0f}")
#    print(f"  + Амортизация: {row['Depreciation']:,.0f}")
#    print(f"  - CAPEX: {row['CAPEX']:,.0f}")
#    print(f"  - ΔWorking Capital: {row['Delta_WC']:,.0f}")
#    print(f"  = FCF: {row['ForecastFCF']:,.0f}")

# Сохранение результатов
df_fcf.to_csv('fcf_forecast.csv', index=False)
#print(f"\nРезультаты сохранены в 'fcf_forecast.csv'")