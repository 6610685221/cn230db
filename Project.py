# นำเข้าไลบรารี requests สำหรับการส่ง HTTP request ไปยัง API
import requests
# นำเข้าไลบรารี sqlite3 สำหรับการทำงานกับฐานข้อมูล SQLite
import sqlite3

# URL ของ Fixer.io API สำหรับดึงข้อมูลอัตราแลกเปลี่ยนล่าสุด
response = requests.get('https://data.fixer.io/api/latest?access_key=622ffa539cd53c3d2410d384a055f9d4')
# แปลงข้อมูลที่ได้รับจาก API (ในรูปแบบ JSON) ให้อยู่ในรูปแบบ dictionary ของ Python
data = response.json()

# เชื่อมต่อกับฐานข้อมูล SQLite ชื่อ 'exchange_rates.db'
conn = sqlite3.connect('exchange_rates.db')
# สร้าง cursor object เพื่อใช้ในการ execute คำสั่ง SQL
cur = conn.cursor()


# สร้างตารางชื่อ 'exchange_rates' หากยังไม่มี
cur.execute('''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        currency TEXT,
        rate REAL,
        date TEXT
    )
''')

# ดึงวันที่ของข้อมูลอัตราแลกเปลี่ยนจากข้อมูลที่ได้จาก API
date = data['date']
# วนลูปผ่านแต่ละสกุลเงินและอัตราแลกเปลี่ยนที่อยู่ใน data['rates']
for currency, rate in data['rates'].items():
    # เพิ่มข้อมูล (currency, rate, date) แถวใหม่เข้าไปในตาราง 'exchange_rates'
    cur.execute('INSERT INTO exchange_rates (currency, rate, date) VALUES (?, ?, ?)', (currency, rate, date))

# บันทึกการเปลี่ยนแปลงทั้งหมด
conn.commit()

# แสดงข้อมูลทั้งหมดที่อยู่ในตาราง exchange_rates
print("Every Exchange Rates data:")
for row in cur.execute("SELECT * FROM exchange_rates "):
    print(row)

# ค้นหาสกุลเงินที่มีอัตราแลกเปลี่ยนต่ำที่สุด
res = cur.execute("SELECT currency, rate FROM exchange_rates ORDER BY rate ASC LIMIT 1")
currency, rate = res.fetchone()
print(f"Currency with min rate: {currency}, Rate: {rate}")

# ค้นหาสกุลเงินที่มีอัตราแลกเปลี่ยนสูงสุด
res = cur.execute("SELECT currency, rate FROM exchange_rates ORDER BY rate DESC LIMIT 1")
currency, rate = res.fetchone()
print(f"Currency with max rate: {currency}, Rate: {rate}")

# คำนวณค่าเฉลี่ยของอัตราแลกเปลี่ยนทั้งหมด
res = cur.execute("SELECT currency, AVG(rate) FROM exchange_rates LIMIT 1")
currency, rate = res.fetchone()
print(f"Average rate of all currencies: {rate}")

# แสดง 5 อันดับสกุลเงินที่มีอัตราแลกเปลี่ยนสูงสุด
print("Top 5 maximum rate:")
for row in cur.execute("SELECT DISTINCT currency, rate FROM exchange_rates ORDER BY rate DESC LIMIT 5"):
    print(row)
    
# แสดง 5 อันดับสกุลเงินที่มีอัตราแลกเปลี่ยนต่ำสุด
print("Top 5 Minimum rate:")
for row in cur.execute("SELECT DISTINCT currency, rate FROM exchange_rates ORDER BY rate ASC LIMIT 5"):
    print(row)

 # ปิดการใช้งาน cursor
cur.close()

 # ปิดการเชื่อมต่อฐานข้อมูล
    conn.close()
    print("\nFinished")
