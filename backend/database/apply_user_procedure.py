import mysql.connector
from mysql.connector import Error

def apply_add_user_procedure():
    try:
        # Database connection configuration
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pegasus@0918',
            database='brightbuy'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # First, create required tables if they don't exist
            create_tables_query = """
            -- Create user table if not exists
            CREATE TABLE IF NOT EXISTS user (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_admin BOOLEAN DEFAULT FALSE,
                UNIQUE INDEX idx_email (email),
                UNIQUE INDEX idx_username (username)
            );

            -- Create address table if not exists
            CREATE TABLE IF NOT EXISTS address (
                address_id INT AUTO_INCREMENT PRIMARY KEY,
                street VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100),
                postal_code VARCHAR(20),
                country VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Create user_address linking table if not exists
            CREATE TABLE IF NOT EXISTS user_address (
                user_id INT,
                address_id INT,
                is_default BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, address_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE
            );
            """
            
            # Execute create tables queries
            for query in create_tables_query.split(';'):
                if query.strip():
                    cursor.execute(query)
            
            # Read and execute the stored procedure
            with open('c:/Users/USER/Desktop/DataBase Project/BrightBuy-Online-Store/backend/database/procedures/add_user_procedure.sql', 'r') as file:
                procedure_query = file.read()
                
            # Execute the stored procedure creation query
            cursor.execute(procedure_query)
            
            connection.commit()
            print("✓ AddUserWithAddress procedure created successfully")
            
    except Error as e:
        print(f"Error creating procedure: {e}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    apply_add_user_procedure()