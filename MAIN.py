import numpy as np
import pandas as pd
from scipy.odr import polynomial
from sklearn.preprocessing import PolynomialFeatures
import datetime as dt

#df_incomes = pd.DataFrame(response_incomes['Information'])
#cols = ['fiscalDateEnding', 'totalRevenue','costofGoodsAndServicesSold',
#       'grossProfit','operatingExpenses','sellingGeneralAndAdministrative',
#      'operatingIncome','interestExpense','ebit','ebitda','netIncome']

def convert_json_to_dataframe(balance_file, income_file):
       df_balance = pd.read_json(balance_file)
       df_income = pd.read_json(income_file)
       return df_balance, df_income,            #--- Dataframe хранится в переменных---

df_balance, df_income = convert_json_to_dataframe('BalanceStatements.json',
                                                  'IncomeStatements.json')

