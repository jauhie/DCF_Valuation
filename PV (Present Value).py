import numpy as np
import pandas as pd
from FCF import df_fcf
from WACC import WACC_corrected

#---PV = FCF_year / (1 + WACC)^(year - 2024)
#---Terminal Value = FCF_2034 × (1 + g) / (WACC - g)
#---PV(Terminal Value) = Terminal Value / (1 + WACC)^5

future_years = np.arange(2025, 2031)
df_PV = pd.DataFrame({'Year':future_years})

wacc_value = WACC_corrected
df_PV['FCF'] = df_fcf['ForecastFCF'].values
df_PV['WACC'] = wacc_value
df_PV['PV'] = df_PV['FCF'] / ((1+df_PV['WACC'])**(future_years-2024))
total_pv = df_PV['PV'].sum()
#print(df_PV['PV'])

g = 0.02
fcf_2030 = df_PV[df_PV['Year'] == 2030]['FCF'].values[0]
terminal_value = fcf_2030 * (1 + g) / (WACC_corrected - g)
pv_terminal = terminal_value / ((1 + WACC_corrected) ** 6)

print(f"Полная стоимость: {total_pv}")
print(f"Терминальная стоимость: {terminal_value:,.0f}")
print(f"PV терминальной стоимости: {pv_terminal:,.0f}")

EnterpriceValue = total_pv + pv_terminal

print(f"Стоимость предприятия: {EnterpriceValue:,.0f}")