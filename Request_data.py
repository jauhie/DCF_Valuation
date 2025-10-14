import json
import requests


api_key2 = 'YA2WLM36IRM85ZFT'
ticker2 = 'OTLY'

#--- Запрос приходящих ключей и их расшифровка (при keyerror)---
#print(response_incomes.keys())
#print(response_incomes.get('Information'))

url_incomes = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker2}&apikey={api_key2}'
response_incomes = requests.get(url_incomes).json()

with open('IncomeStatements.json','r') as f:
    json.dump(response_incomes, f, indent=4)

url_balance = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker2}&apikey={api_key2}'
responce_balance = requests.get(url_balance).json()

with open('BalanceStatements.json','r') as f:
    json.dump(responce_balance, f, indent=4)


