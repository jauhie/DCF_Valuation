import yfinance as yf
import pandas as pd

ticker = "OTLY"
stock = yf.Ticker(ticker)
info = stock.info

print(f"=== {ticker} БАЗОВАЯ ИНФОРМАЦИЯ ===")
print(f"Компания: {info.get('longName')}")
print(f"Цена: {info.get('currentPrice')} $")
print(f"Капитализация: {info.get('marketCap'):,} $")

revenue = info.get('totalRevenue', 0)
net_income = info.get('netIncome', 0)

print(f"\n=== ОСНОВНЫЕ МУЛЬТИПЛИКАТОРЫ ===")
print(f"Выручка: {revenue:,.0f} $")
print(f"Чистая прибыль: {net_income:,.0f} $")

# Считаем P/S и P/E
if revenue > 0:
    ps_ratio = info.get('marketCap') / revenue
    print(f"P/S (цена/выручка): {ps_ratio:.2f}")

if net_income > 0:
    pe_ratio = info.get('marketCap') / net_income
    print(f"P/E (цена/прибыль): {pe_ratio:.2f}")

# Сравниваем с парой аналогов
analogs = ['BYND', 'DNUT']
print(f"\n=== СРАВНЕНИЕ С АНАЛОГАМИ {analogs} ===")

for analog in analogs:
    try:
        a_stock = yf.Ticker(analog)
        a_info = a_stock.info
        a_revenue = a_info.get('totalRevenue', 0)

        if a_revenue > 0:
            a_ps = a_info.get('marketCap') / a_revenue
            print(f"{analog}: P/S = {a_ps:.2f}")
    except:
        print(f"{analog}: нет данных")


print(f"\n=== ОЦЕНКА ===")
if revenue > 0:
    # Средний P/S по аналогам ~1.5x (типично для пищевых компаний)
    fair_value = revenue * 1.5
    current_value = info.get('marketCap')

    print(f"Текущая стоимость: {current_value:,.0f} $")
    print(f"Справедливая стоимость: {fair_value:,.0f} $")

    difference = (fair_value - current_value) / current_value * 100
    print(f"Разница: {difference:+.1f}%")

    if difference > 10:
        print("Вывод: ВЕРОЯТНО НЕДООЦЕНЕН")
    elif difference < -10:
        print("Вывод: ВЕРОЯТНО ПЕРЕОЦЕНЕН")
    else:
        print("Вывод: СПРАВЕДЛИВАЯ ЦЕНА")