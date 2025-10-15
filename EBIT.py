import pandas as pd
import numpy as np
from Revenue import df_revenue_pred

df_forecast_ebit = pd.DataFrame({'Year': np.array([2025,2026,2027,2028,2029,2030]),
                                 'PredictedRevenue': df_revenue_pred['PredictedRevenue']})
#---EBIT = Revenue - COGS - OPEX