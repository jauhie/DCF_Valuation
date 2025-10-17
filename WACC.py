import yfinance as yf

ticker = yf.Ticker("OTLY")
info = ticker.info
annual_balance_sheet = ticker.balance_sheet

market_cap = info.get('marketCap')
total_debt = info.get('totalDebt')
beta = info.get('beta')
cash = annual_balance_sheet.loc['Cash And Cash Equivalents'].iloc[0]
cost_of_debt = 0.095
TaxRate_sweden = 0.21
RiskFreeRate_USA = 0.043


enterprise_value_corrected = market_cap + total_debt - cash
market_debt_corrected = total_debt  # Используем балансовую стоимость

# Расчет средневзвешенной премии за риск
RickPremium = {'EU':{'RiskPremium':5, 'revenue_share':0.5},
               'USA':{'RiskPremium':6, 'revenue_share':0.33},
               'China':{'RiskPremium':8.2, 'revenue_share':0.16}}

weighted_premium = 0
for region, data in RickPremium.items():
    weighted_premium += data['RiskPremium'] * data['revenue_share']

CAMP = RiskFreeRate_USA + (beta * (weighted_premium/100))

# Расчет WACC с исправленными данными
total_value_corrected = market_cap + market_debt_corrected
weight_equity_corrected = market_cap / total_value_corrected
weight_debt_corrected = market_debt_corrected / total_value_corrected

WACC_corrected = ((weight_equity_corrected * CAMP) +
                  (weight_debt_corrected * cost_of_debt * (1 - TaxRate_sweden)))
