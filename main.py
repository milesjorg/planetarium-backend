from fastapi import FastAPI
from skyfield.api import load
from datetime import datetime

app = FastAPI()

# Load once
planets = load('de421.bsp')
ts = load.timescale()

@app.get("/planet/{name}")
def get_planet_position(name: str):
    name = name.lower()

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