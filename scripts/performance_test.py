import time
import mysql.connector
import os

# MySQL connection configuration
DB_CONFIG = {
    'user': os.environ.get('DBUSER', 'root'),
    'password': os.environ.get('DBPASS', 'Secret5555'),
    'host': os.environ.get('DBHOST', '127.0.0.1'),
    'database': os.environ.get('DBNAME', 'olist_ecommerce')
}

QUERIES = [
    {
        'name': 'Scalar - AVG payment_value',
        'sql': "SELECT AVG(payment_value) FROM payments;"
    },
    {
        'name': 'Scalar - WHERE payment_value > 100',
        'sql': "SELECT * FROM payments WHERE payment_value > 100;"
    },
    {
        'name': 'Scalar - WHERE freight_value > 20',
        'sql': "SELECT * FROM order_items WHERE freight_value > 20;"
    },
    {
        'name': 'Full-text - LIKE search',
        'sql': "SELECT * FROM reviews WHERE review_comment_message LIKE '%atraso%';"
    },
    {
        'name': 'Full-text - MATCH AGAINST',
        'sql': "SELECT * FROM reviews WHERE MATCH(review_comment_message) AGAINST('atraso entrega' IN NATURAL LANGUAGE MODE);"
    }
]

def run_queries():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Running performance tests...\n")
        for q in QUERIES:
            print(f"Running: {q['name']}")
            start = time.perf_counter()
            cursor.execute(q['sql'])
            _ = cursor.fetchall()
            duration = time.perf_counter() - start
            print(f"Time: {duration:.4f} seconds\n")

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
    finally:
        if cursor: cursor.close()
        if conn.is_connected(): conn.close()

if __name__ == "__main__":
    run_queries()
