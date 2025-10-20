
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'brightbuy')
DB_PORT = int(os.getenv('DB_PORT', 3306))

# Database connection configuration
DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'port': DB_PORT,
    'autocommit': False,
    'raise_on_warnings': True
}

# Create connection pool for better performance
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="brightbuy_pool",
    pool_size=10,
    pool_reset_session=True,
    **DB_CONFIG
)

def get_connection():
    """
    Get a connection from the pool.
    Returns a mysql.connector connection object.
    """
    return connection_pool.get_connection()

def get_db():
    """
    Dependency function to get database connection.
    Returns a mysql.connector connection object with dictionary cursor.
    """
    connection = connection_pool.get_connection()
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()