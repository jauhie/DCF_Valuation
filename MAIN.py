import pandas as pd
import requests

api_key = 'W8ZBNCNKKDOM92U0'
ticker = 'OTLY'


url_incomes = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}'
response_incomes = requests.get(url_incomes).json()

url_balance = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}'
responce_balance = requests.get(url_balance).json()

#url_cashflow = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
#responce_cashflow = requests.get(url_cashflow).json()


"""Формирование датасета из отчета о прибылях и убытках за все года"""

df_incomes = pd.DataFrame(response_incomes['annualReports'])
cols = ['fiscalDateEnding', 'totalRevenue','costofGoodsAndServicesSold',
        'grossProfit','operatingExpenses','sellingGeneralAndAdministrative',
        'operatingIncome','interestExpense','ebit','ebitda','netIncome']

existing_incomes = [c for c in cols if c in df_incomes.columns]
print(df_incomes[existing_incomes])
#print(df.columns.tolist())

"""Формирование датасета из балансового отчёта"""

df_balance = pd.DataFrame(responce_balance['annualReports'])
print(df_balance.columns.tolist())


