import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Pegasus@0918',
        database='brightbuy'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Show all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in the database.")
        else:
            print("\nTables in 'brightbuy' database:")
            print("-" * 40)
            for table in tables:
                print(f"• {table[0]}")
                # Show table structure
                cursor.execute(f"DESCRIBE {table[0]}")
                columns = cursor.fetchall()
                print("\nColumns:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
                print("-" * 40)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed")