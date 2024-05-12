import mysql.connector
import os
from dotenv import load_dotenv

def execute_sql_from_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
        commands = sql.split(';')[:-1]  # Split by ';' and remove the last empty command
        for command in commands:
            try:
                cursor.execute(command + ';')  # Add ';' to complete the command
            except mysql.connector.Error as err:
                print(f"Failed executing command: {command} Error: {err}")

def main():
    load_dotenv()  # Load environment variables from .env file

    # Database connection details
    db_config = {
        'host': os.getenv("MYSQL_HOST"),
        'user': os.getenv("MYSQL_USER"),
        'password': os.getenv("MYSQL_PASSWORD"),
        'database': os.getenv("MYSQL_DATABASE")
    }

    try:
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS api_keys;")
        cursor.execute("DROP TABLE IF EXISTS individuals;")
        cursor.execute("DROP TABLE IF EXISTS companies;")
        cursor.execute("DROP TABLE IF EXISTS places;")
        print("Existing tables dropped successfully.")

        # Execute DDL SQL from files
        execute_sql_from_file(cursor, 'db_schema/api_keys.sql')
        execute_sql_from_file(cursor, 'db_schema/places.sql')
        execute_sql_from_file(cursor, 'db_schema/companies.sql')
        execute_sql_from_file(cursor, 'db_schema/individuals.sql')
        
        db.commit()
        print("New tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    main()

