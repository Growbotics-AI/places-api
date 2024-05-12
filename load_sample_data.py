import os
import logging
import argparse
import requests  # Using requests for HTTP calls
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get API key and API URL from .env
api_key = os.getenv("PLACES_API_KEY")
api_base_url = os.getenv(
    "PLACES_API_URL", "http://localhost:8001"
)  # Default to localhost if not set


# Function to delete data via API call
def clear_tables():
    api_url = (
        f"{api_base_url}/clear-all-data"  # Dynamic URL based on environment variable
    )
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        logging.info("Data cleared from all tables successfully.")
        print(response.json())  # Print the response from the server
    else:
        logging.error(f"Failed to clear data: {response.text}")


def insert_sample_data():
    companies_url = f"{api_base_url}/companies"  # URL for the companies endpoint
    individuals_url = f"{api_base_url}/individuals"  # URL for the individuals endpoint
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    # List containing both companies and individuals
    entities = [
        {
            "type": "company",
            "data": {
                "name": "Digital Manufacturing Inc.",
                "website": "http://www.digitalmanufacturinginc.com",
                "email": "info@digitalmanufacturinginc.com",
                "place": {
                    "position": [52.051977014580125, 8.531494086782844],
                    "title": "Digital Manufacturing Inc.",
                    "address": "Industry Park 123, Tech City",
                    "category": "DIGITAL_FACTORY",
                },
            },
        },
        {
            "type": "company",
            "data": {
                "name": "TechStore Retail",
                "website": "http://www.techstoreretail.com",
                "email": "sales@techstoreretail.com",
                "place": {
                    "position": [52.01219274931668, 8.599568218099812],
                    "title": "TechStore Retail",
                    "address": "Retail District 131415, Tech City",
                    "category": "TECHNO_FARMER",
                },
            },
        },
        {
            "type": "individual",
            "data": {
                "first_name": "Alex",
                "last_name": "Smith",
                "email": "alex.smith@assembleworks.com",
                "place": {
                    "position": [52.022468698328275, 8.50583167463131],
                    "title": "AssembleWorks",
                    "address": "Assembly Line 789, Tech City",
                    "category": "ROBOSMITH",
                },
            },
        },
        {
            "type": "individual",
            "data": {
                "first_name": "Megan",
                "last_name": "Browning",
                "email": "megan.b@mechanicshub.com",
                "place": {
                    "position": [51.99739839338658, 8.59544834428681],
                    "title": "Mechanics Hub",
                    "address": "Maker Space 101112, Tech City",
                    "category": "ROBOSMITH",
                },
            },
        },
    ]

    for entity in entities:
        if entity["type"] == "company":
            response = requests.post(
                companies_url, headers=headers, data=json.dumps(entity["data"])
            )
            action = "Company added"
        elif entity["type"] == "individual":
            response = requests.post(
                individuals_url, headers=headers, data=json.dumps(entity["data"])
            )
            action = "Individual added"

        if response.status_code == 200:
            print(f"{action} successfully:", response.json())
        else:
            logging.error(f"Error posting data: {response.text}")


def test_api():
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    # Test data for different operations
    company_data = json.dumps(
        {
            "name": "New Company",
            "website": "https://newcompany.com",
            "email": "contact@newcompany.com",
            "place": {
                "position": [52.5200, 13.4050],
                "title": "New Place",
                "address": "New Address, City",
                "category": "DIGITAL_FACTORY",
            },
        }
    )

    individual_data = json.dumps(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "place": {
                "position": [52.5200, 13.4050],
                "title": "Individuals Place",
                "address": "Some Address, City",
                "category": "TECHNO_FARMER",
            },
        }
    )

    # Test adding a company
    logging.info("Testing Adding a Company with a new place...")
    response = requests.post(
        f"{api_base_url}/companies", headers=headers, data=company_data
    )
    print("Add Company Response:", response.text)

    # Test adding an individual
    logging.info("Testing Adding an Individual with a new place...")
    response = requests.post(
        f"{api_base_url}/individuals", headers=headers, data=individual_data
    )
    print("Add Individual Response:", response.text)

    # Test updating a company
    logging.info("Testing Updating a Company...")
    company_update_data = json.dumps(
        {
            "name": "Updated Company",
            "website": "https://updatedcompany.com",
            "email": "updated@updatedcompany.com",
            "place": {
                "position": [52.5200, 13.4050],  # Example position
                "title": "Updated Place",
                "address": "Updated Address, City",
                "category": "DIGITAL_FACTORY",
            },
        }
    )
    response = requests.put(
        f"{api_base_url}/companies/1", headers=headers, data=company_update_data
    )
    print("Update Company Response:", response.text)

    # Test deleting a company
    logging.info("Testing Deleting a Company...")
    response = requests.delete(f"{api_base_url}/companies/1", headers=headers)
    print("Delete Company Response:", response.text)

    # Test getting nearby places
    logging.info("Testing Getting Nearby Places...")
    response = requests.get(
        f"{api_base_url}/places/nearby?lat=52.5200&lng=13.4050&radius=1000",
        headers=headers,
    )
    print("Nearby Places Response:", response.text)

    logging.info("Testing Complete")


# Setting up command line arguments
parser = argparse.ArgumentParser(description="Sample Data Management Script")
parser.add_argument("--delete", help="Delete data from tables", action="store_true")
parser.add_argument(
    "--load", help="Load sample data into the database", action="store_true"
)
parser.add_argument(
    "--reload",
    help="Reload data into the database (delete then load)",
    action="store_true",
)
parser.add_argument("--test-api", help="Test API endpoints", action="store_true")

# Check if any arguments were passed; if not, print help
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Main execution
if __name__ == "__main__":
    args = parser.parse_args()
    if args.delete:
        clear_tables()
    elif args.load:
        insert_sample_data()
    elif args.reload:
        clear_tables()
        insert_sample_data()
    elif args.test_api:
        test_api()
