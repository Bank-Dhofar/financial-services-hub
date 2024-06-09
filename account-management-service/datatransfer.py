from pymongo import MongoClient
import psycopg2
from psycopg2 import sql

def transfer_data():
    # Connect to MongoDB
    mongo_client = MongoClient('mongodb://localhost:27017/')
    mongo_db = mongo_client['bank']
    users_collection = mongo_db['user_data']

    # Connect to PostgreSQL
    pg_connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="reporting")
    pg_cursor = pg_connection.cursor()

    # Create a temporary table in PostgreSQL to store data from MongoDB
    pg_cursor.execute("""
        CREATE TEMPORARY TABLE temp_user_info (
            name VARCHAR(255),
            account_number VARCHAR(255),
            balance NUMERIC
        )
    """)

    # Insert data from MongoDB into the temporary table
    for user in users_collection.find():
        pg_cursor.execute("""
            INSERT INTO temp_user_info (name, account_number, balance)
            VALUES (%s, %s, %s)
        """, (user['name'], user['account_number'], user['balance']))

    # Update or insert records in the main table based on the data in the temporary table
    upsert_query = sql.SQL("""
        INSERT INTO user_info (name, account_number, balance)
        SELECT tu.name, tu.account_number, tu.balance
        FROM temp_user_info tu
        ON CONFLICT (account_number) DO UPDATE
        SET name = EXCLUDED.name,
            balance = EXCLUDED.balance
    """)
    pg_cursor.execute(upsert_query)

    # Commit the transaction and close connections
    pg_connection.commit()
    pg_cursor.close()
    pg_connection.close()
    mongo_client.close()

if __name__ == "__main__":
    transfer_data()
