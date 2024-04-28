from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Category(str, Enum):
    DIGITAL_FACTORIES = "DIGITAL_FACTORIES"
    ROBOSMITHS = "ROBOSMITHS"
    TECHNO_FARMERS = "TECHNO_FARMERS"

class Place(BaseModel):
    id: int
    position: list[float]
    category: Category
    title: str
    address: str

places = [
    Place(
        id=1,
        position=[52.051977014580125, 8.531494086782844],
        category=Category.DIGITAL_FACTORIES,
        title="Digital Manufacturing Inc.",
        address="Industry Park 123, Tech City",
    ),
    Place(
        id=2,
        position=[52.02022592597971, 8.530780645829076],
        category=Category.DIGITAL_FACTORIES,
        title="3D Print World",
        address="Innovation Street 56, Tech City",
    ),
    Place(
        id=3,
        position=[52.022468698328275, 8.50583167463131],
        category=Category.ROBOSMITHS,
        title="AssembleWorks",
        address="Assembly Line 789, Tech City",
    ),
    Place(
        id=4,
        position=[51.99739839338658, 8.59544834428681],
        category=Category.ROBOSMITHS,
        title="Mechanics Hub",
        address="Maker Space 101112, Tech City",
    ),
    Place(
        id=5,
        position=[52.01219274931668, 8.599568218099812],
        category=Category.TECHNO_FARMERS,
        title="TechStore Retail",
        address="Retail District 131415, Tech City",
    ),
    Place(
        id=6,
        position=[52.0119, 8.563032],
        category=Category.TECHNO_FARMERS,
        title="InnoShop Electronics",
        address="Downtown 161718, Tech City",
    ),
    Place(
        id=7,
        position=[51.5074, -0.1278],  # Coordinates for Central London
        category=Category.DIGITAL_FACTORIES,
        title="London Tech Foundry",
        address="Tech Park, Central London",
    ),
    Place(
        id=8,
        position=[51.5155, -0.0922],  # Coordinates near the London Bridge
        category=Category.ROBOSMITHS,
        title="Robotics Innovation Lab",
        address="Robotic Way 221, Near London Bridge",
    ),
    Place(
        id=9,
        position=[51.5245, -0.1340],  # Coordinates near the British Museum
        category=Category.TECHNO_FARMERS,
        title="GreenTech Gardens",
        address="Cultivation Court 321, Bloomsbury",
    ),
    Place(
        id=10,
        position=[51.5128, -0.0910],  # Coordinates near the Tower of London
        category=Category.TECHNO_FARMERS,
        title="TechGrow Hub",
        address="Heritage Site 424, East London",
    ),
]

@app.get("/places")
def get_places():
    return places