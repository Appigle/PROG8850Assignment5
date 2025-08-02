import mysql.connector
import os

# MySQL connection configuration
DB_CONFIG = {
    'user': os.environ.get('DBUSER', 'root'),
    'password': os.environ.get('DBPASS', 'Secret5555'),
    'host': os.environ.get('DBHOST', '127.0.0.1'),
    'database': os.environ.get('DBNAME', 'olist_ecommerce')
}

# Tables to count
TABLES = [
    'customers',
    'geolocation',
    'orders',
    'order_items',
    'payments',
    'reviews',
    'products',
    'sellers',
    'product_category_translation'
]

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("📊 Total row counts per table:\n")

    for table in TABLES:
        query = f"SELECT COUNT(*) FROM {table}"
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"{table:<30}: {result[0]} rows")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals() and conn.is_connected(): conn.close()
