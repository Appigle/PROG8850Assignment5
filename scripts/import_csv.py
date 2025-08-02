import csv
import mysql.connector
import os

# MySQL connection parameters
DB_CONFIG = {
    'user': os.environ.get('DBUSER', 'root'),
    'password': os.environ.get('DBPASS', 'Secret5555'),
    'host': os.environ.get('DBHOST', '127.0.0.1'),
    'database': os.environ.get('DBNAME', 'olist_ecommerce')
}

CSV_FOLDER = 'Brazilian-E-Commerce-Public-Dataset-by-Olist'

FILES_AND_TABLES = [
    {
        'filename': 'olist_customers_dataset.csv',
        'table': 'customers',
        'columns': ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']
    },
    {
        'filename': 'olist_geolocation_dataset.csv',
        'table': 'geolocation',
        'columns': ['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state']
    },
    {
        'filename': 'olist_orders_dataset.csv',
        'table': 'orders',
        'columns': ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_approved_at',
                    'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    },
    {
        'filename': 'olist_order_items_dataset.csv',
        'table': 'order_items',
        'columns': ['order_id', 'order_item_id', 'product_id', 'seller_id', 'shipping_limit_date', 'price', 'freight_value']
    },
    {
        'filename': 'olist_order_payments_dataset.csv',
        'table': 'payments',
        'columns': ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value']
    },
    {
        'filename': 'olist_order_reviews_dataset.csv',
        'table': 'reviews',
        'columns': ['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message',
                    'review_creation_date', 'review_answer_timestamp']
    },
    {
        'filename': 'olist_products_dataset.csv',
        'table': 'products',
        'columns': ['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght',
                    'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    },
    {
        'filename': 'olist_sellers_dataset.csv',
        'table': 'sellers',
        'columns': ['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']
    },
    {
        'filename': 'product_category_name_translation.csv',
        'table': 'product_category_translation',
        'columns': ['product_category_name', 'product_category_name_english']
    }
]

try:
    cnx = mysql.connector.connect(**DB_CONFIG)
    cursor = cnx.cursor()

    for item in FILES_AND_TABLES:
        file_path = os.path.join(CSV_FOLDER, item['filename'])
        table = item['table']
        columns = item['columns']

        print(f"\nImporting '{file_path}' into table '{table}'...")

        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)

            for row in csv_reader:
                row = [col if col != '' else None for col in row]  # Handle empty values
                try:
                    cursor.execute(insert_sql, row)
                except Exception as e:
                    print(f"Error inserting into {table}: {e}\nRow: {row}")

        cnx.commit()
        print(f"{table}: {cursor.rowcount} rows inserted.")

except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
    print("\nAll data import tasks completed.")
