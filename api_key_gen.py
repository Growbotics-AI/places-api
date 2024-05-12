import mysql.connector
import os
from dotenv import load_dotenv
import secrets
import logging
import argparse
import sys  # Import sys to check for command line arguments

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"), 
        user=os.getenv("MYSQL_USER"), 
        password=os.getenv("MYSQL_PASSWORD"), 
        database=os.getenv("MYSQL_DATABASE")
    )

# Function to generate an API key
def generate_api_key(description):
    api_key = secrets.token_urlsafe(32)  # Generate a secure random API key
    return api_key, description

# Function to insert API key into the database
def store_api_key(api_key, description, is_active=True):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO api_keys (api_key, description, is_active) VALUES (%s, %s, %s)"
    cursor.execute(query, (api_key, description, is_active))
    db.commit()
    cursor.close()
    db.close()
    logging.info("API key stored successfully: %s", api_key)

# Function to list all API keys
def list_api_keys():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT api_key, description, is_active FROM api_keys")
    keys = cursor.fetchall()
    cursor.close()
    db.close()
    for key in keys:
        print(f"API Key: {key[0]}, Description: {key[1]}, Active: {key[2]}")

# Function to update an API key's active status
def update_api_key_status(api_key, is_active):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE api_keys SET is_active = %s WHERE api_key = %s", (is_active, api_key))
    db.commit()
    cursor.close()
    db.close()
    logging.info("API key status updated: %s", api_key)

# Function to delete an API key
def delete_api_key(api_key):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM api_keys WHERE api_key = %s", (api_key,))
    db.commit()
    cursor.close()
    db.close()
    logging.info("API key deleted: %s", api_key)

# Argument parser setup
parser = argparse.ArgumentParser(description="API Key Management Script")
parser.add_argument("--list", help="List all API keys", action="store_true")
parser.add_argument("--generate", help="Generate a new API key", metavar="DESCRIPTION")
parser.add_argument("--update", help="Update an API key's active status", nargs=2, metavar=("API_KEY", "IS_ACTIVE"))
parser.add_argument("--delete", help="Delete an API key", metavar="API_KEY")

# Check if any arguments were passed; if not, print help
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Main execution
if __name__ == "__main__":
    args = parser.parse_args()
    if args.list:
        list_api_keys()
    elif args.generate:
        key, desc = generate_api_key(args.generate)
        store_api_key(key, desc)
        print(f"Generated API Key: {key}")
        print(f"Description: {desc}")
    elif args.update:
        update_api_key_status(args.update[0], bool(int(args.update[1])))
    elif args.delete:
        delete_api_key(args.delete)
