# app/drone_scenarios.py

import random

DRONE_SCENARIOS = [
    {
        "location": "RedwoodForest",
        "severity": "HighSeverity",
        "fireSpreadRate": 8.5,
        "airQuality": 210,
        "visibleFlames": 15.3
    },
    {
        "location": "BlueRidge",
        "severity": "ModerateSeverity",
        "fireSpreadRate": 3.2,
        "airQuality": 120,
        "visibleFlames": 9.1
    },
    {
        "location": "SunsetValley",
        "severity": "LowSeverity",
        "fireSpreadRate": 1.2,
        "airQuality": 50,
        "visibleFlames": 4.5
    }
]

def get_random_drone_report():
    return random.choice(DRONE_SCENARIOS)
