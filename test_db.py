import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host="193.233.216.12",      # например 185.113.132.123
    port=5432,
    database="fitness_crm",
    user="admin",
    password="admin"  # твой пароль
)

cur = conn.cursor()
cur.execute("SELECT version();")
print("✅ PostgreSQL версия:", cur.fetchone()[0])

# Тест таблицы
cur.execute("""
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        test_data VARCHAR(50)
    )
""")
cur.execute("INSERT INTO test_table (test_data) VALUES ('CRM бот работает!')")
conn.commit()

cur.execute("SELECT * FROM test_table;")
print("✅ Данные:", cur.fetchall())

cur.close()
conn.close()
print("✅ Подключение успешно!")


