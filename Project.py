import requests
import sqlite3

response = requests.get('https://data.fixer.io/api/latest?access_key=622ffa539cd53c3d2410d384a055f9d4')
data = response.json()

conn = sqlite3.connect('exchange_rates.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        currency TEXT,
        rate REAL,
        date TEXT
    )
''')

date = data['date']
for currency, rate in data['rates'].items():
    cur.execute('INSERT INTO exchange_rates (currency, rate, date) VALUES (?, ?, ?)', (currency, rate, date))

conn.commit()

for row in cur.execute("SELECT * FROM exchange_rates "):
    print(row)

res = cur.execute("SELECT currency, rate FROM exchange_rates ORDER BY rate ASC LIMIT 1")
currency, rate = res.fetchone()
print(f"Currency with min rate: {currency}, Rate: {rate}")

res = cur.execute("SELECT currency, rate FROM exchange_rates ORDER BY rate DESC LIMIT 1")
currency, rate = res.fetchone()
print(f"Currency with max rate: {currency}, Rate: {rate}")

res = cur.execute("SELECT currency, AVG(rate) FROM exchange_rates LIMIT 1")
currency, rate = res.fetchone()
print(f"Average rate of all currencies: {rate}")

print("Top 5 maximum rate:")
for row in cur.execute("SELECT DISTINCT currency, rate FROM exchange_rates ORDER BY rate DESC LIMIT 5"):
    print(row)

print("Top 5 Minimum rate:")
for row in cur.execute("SELECT DISTINCT currency, rate FROM exchange_rates ORDER BY rate ASC LIMIT 5"):
    print(row)


cur.close()

