from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
import mysql.connector
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file.

logging.basicConfig(level=logging.DEBUG)


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


# Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(api_key: APIKey = Depends(api_key_header)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT * FROM api_keys WHERE api_key = %s AND is_active = 1", (api_key,)
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=403, detail="Invalid API key")
    finally:
        cursor.close()
        db.close()


app = FastAPI()


# Models
class Place(BaseModel):
    position: list[float]
    title: str
    address: str
    category: str


class Company(BaseModel):
    name: str
    website: str
    email: str
    place: Place


class Individual(BaseModel):
    first_name: str
    last_name: str
    email: str
    place: Place


# Endpoints
@app.post("/companies")
def add_company(company: Company, api_key: APIKey = Depends(verify_api_key)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO places (position, title, address, category) VALUES (ST_GeomFromText('POINT(%s %s)'), %s, %s, %s)",
        (
            company.place.position[0],
            company.place.position[1],
            company.place.title,
            company.place.address,
            company.place.category,
        ),
    )
    place_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO companies (place_id, name, website, email) VALUES (%s, %s, %s, %s)",
        (place_id, company.name, company.website, company.email),
    )
    db.commit()
    return {"message": "Company added successfully"}


@app.put("/companies/{id}")
def update_company(
    id: int, company: Company, api_key: APIKey = Depends(verify_api_key)
):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE companies SET name=%s, website=%s, email=%s WHERE id=%s",
        (company.name, company.website, company.email, id),
    )
    db.commit()
    return {"message": "Company updated successfully"}


@app.delete("/companies/{id}")
def delete_company(id: int, api_key: APIKey = Depends(verify_api_key)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM companies WHERE id=%s", (id,))
    db.commit()
    return {"message": "Company deleted successfully"}


@app.post("/individuals")
def add_individual(individual: Individual, api_key: APIKey = Depends(verify_api_key)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO places (position, title, address, category) VALUES (ST_GeomFromText('POINT(%s %s)'), %s, %s, %s)",
        (
            individual.place.position[0],
            individual.place.position[1],
            individual.place.title,
            individual.place.address,
            individual.place.category,
        ),
    )
    place_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO individuals (place_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)",
        (place_id, individual.first_name, individual.last_name, individual.email),
    )
    db.commit()
    return {"message": "Individual added successfully"}


@app.put("/individuals/{id}")
def update_individual(
    id: int, individual: Individual, api_key: APIKey = Depends(verify_api_key)
):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE individuals SET first_name=%s, last_name=%s, email=%s WHERE id=%s",
        (individual.first_name, individual.last_name, individual.email, id),
    )
    db.commit()
    return {"message": "Individual updated successfully"}


@app.delete("/individuals/{id}")
def delete_individual(id: int, api_key: APIKey = Depends(verify_api_key)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM individuals WHERE id=%s", (id,))
    db.commit()
    return {"message": "Individual deleted successfully"}


@app.get("/places/nearby")
async def get_nearby_places(
    lat: float, lng: float, radius: float, api_key: APIKey = Depends(verify_api_key)
):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = f"""
    SELECT p.id,
           JSON_ARRAY(ST_X(p.position), ST_Y(p.position)) AS position,  # Ensuring array format
           p.title,
           p.address,
           CASE p.category
               WHEN 'DIGITAL_FACTORY' THEN 'DIGITAL_FACTORIES'
               WHEN 'ROBOSMITH' THEN 'ROBOSMITHS'
               WHEN 'TECHNO_FARMER' THEN 'TECHNO_FARMERS'
               ELSE p.category
           END AS category,
           ST_Distance_Sphere(p.position, ST_GeomFromText('POINT({lat} {lng})')) as distance,
           CASE
               WHEN c.name IS NOT NULL THEN c.name
               WHEN i.first_name IS NOT NULL THEN CONCAT(i.first_name, ' ', i.last_name)
               ELSE NULL
           END AS name,
           CASE
               WHEN c.name IS NOT NULL THEN c.website
               ELSE NULL
           END AS website,
           CASE
               WHEN c.name IS NOT NULL THEN c.email
               WHEN i.first_name IS NOT NULL THEN i.email
               ELSE NULL
           END AS email,
           CASE
               WHEN c.name IS NOT NULL THEN 'company'
               WHEN i.first_name IS NOT NULL THEN 'individual'
               ELSE NULL
           END AS type
    FROM places p
    LEFT JOIN companies c ON p.id = c.place_id
    LEFT JOIN individuals i ON p.id = i.place_id
    WHERE ST_Distance_Sphere(p.position, ST_GeomFromText('POINT({lat} {lng})')) <= {radius}
    ORDER BY distance ASC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    # Ensure positions are returned as arrays of numbers
    for result in results:
        result["position"] = json.loads(result["position"])
    return results


@app.delete("/clear-all-data")
def clear_all_data(api_key: APIKey = Depends(verify_api_key)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Delete data in a specific order to handle foreign key constraints if present
        cursor.execute("DELETE FROM companies;")
        cursor.execute("DELETE FROM individuals;")
        cursor.execute("DELETE FROM places;")
        db.commit()
        return {"message": "All data cleared successfully"}
    except mysql.connector.Error as err:
        db.rollback()  # Ensures that the database is not partially modified
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
