from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from skyfield.api import load
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load once
planets = load('de421.bsp')
ts = load.timescale()

skyfield_names = {
        'mercury': 'mercury',
        'venus': 'venus',
        'earth': 'earth',
        'mars': 'mars',
        'jupiter': 'jupiter barycenter',
        'saturn': 'saturn barycenter',
        'uranus': 'uranus barycenter',
        'neptune': 'neptune barycenter',
        'pluto': 'pluto barycenter'
    }

PLANETS = {
    "mercury": {
        "semi_major_axis_au": 0.387098,
        "eccentricity": 0.2056,
        "orbital_period_days": 87.97
    },
    "venus": {
        "semi_major_axis_au": 0.723332,
        "eccentricity": 0.0067,
        "orbital_period_days": 224.70
    },
    "earth": {
        "semi_major_axis_au": 1.000003,
        "eccentricity": 0.0167,
        "orbital_period_days": 365.25
    },
    "mars": {
        "semi_major_axis_au": 1.523679,
        "eccentricity": 0.0934,
        "orbital_period_days": 686.98
    },
    "jupiter": {
        "semi_major_axis_au": 5.202603,
        "eccentricity": 0.0489,
        "orbital_period_days": 4332.59
    },
    "saturn": {
        "semi_major_axis_au": 9.537070,
        "eccentricity": 0.0565,
        "orbital_period_days": 10759.22
    },
    "uranus": {
        "semi_major_axis_au": 19.191263,
        "eccentricity": 0.0463,
        "orbital_period_days": 30688.5
    },
    "neptune": {
        "semi_major_axis_au": 30.068963,
        "eccentricity": 0.0095,
        "orbital_period_days": 60182
    },
    "pluto": {
        "semi_major_axis_au": 39.481686,
        "eccentricity": 0.2488,
        "orbital_period_days": 90560
    }
}

@app.get("/planet/{name}")
def get_planet_position(name: str):
    name = name.lower()

    if name not in skyfield_names:
        return {"error": "Planet not found"}

    planet = planets[skyfield_names[name]]
    t = ts.now()
    position = planet.at(t).position.au

    return {
        "planet": name,
        "timestamp": t.utc_iso(),
        "x": position[0],
        "y": position[1],
        "z": position[2]
    }

@app.get("/planet/{name}/orbit")
def get_planet_orbit(name: str):
    name = name.lower()

    if name not in PLANETS:
        return {"error": "Planet not found"}

    return PLANETS[name]    


@app.get("/planets")
def get_all_planet_positions(time: Optional[str] = None):
    if time:
        try:
            dt = datetime.fromisoformat(time)
        except ValueError:
            return {"error": "time must be an ISO-8601 string, e.g. 2023-01-02T15:04:05"}
        t = ts.from_datetime(dt)
    else:
        t = ts.now()
    output = []

    for key, skyfield_name in skyfield_names.items():
        planet = planets[skyfield_name]
        position = planet.at(t).position.au
        output.append({
            "planet": key,
            "x": position[0],
            "y": position[1],
            "z": position[2]
        })

    return {
        "timestamp": t.utc_iso(),
        "planets": output
    }
