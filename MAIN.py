import numpy as np
import pandas as pd
import requests
from scipy.odr import polynomial
from sklearn.preprocessing import PolynomialFeatures
import json


"""Формирование датасета из отчета о прибылях и убытках за все года"""

df_incomes = pd.DataFrame(response_incomes['Information'])
cols = ['fiscalDateEnding', 'totalRevenue','costofGoodsAndServicesSold',
       'grossProfit','operatingExpenses','sellingGeneralAndAdministrative',
       'operatingIncome','interestExpense','ebit','ebitda','netIncome']

