import pandas as pd
from COGS import df_cogs_forecast
from OPEX import df_opex_forecast
from Revenue import df_revenue_pred

#---EBIT = Revenue - COGS - OPEX---

df = pd.concat([df_opex_forecast['Year'],
                              df_revenue_pred['PredictedRevenue'],
                              df_cogs_forecast['PredictedCOGS'],
                              df_opex_forecast['PredictedOpex']], axis=1)

df['ForecastEBIT'] = (df_revenue_pred['PredictedRevenue']
                                    - df_cogs_forecast['PredictedCOGS']
                                    - df_opex_forecast['PredictedOpex'])

df_ebit_forecast = pd.concat([
    df_opex_forecast['Year'],
    df_revenue_pred['PredictedRevenue'],
    df_cogs_forecast['PredictedCOGS'],
    df_opex_forecast['PredictedOpex'],
    df['ForecastEBIT']], axis=1)
