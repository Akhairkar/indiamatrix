import json
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

history_data = {
    "population": {
        "title": "Population (in billions)",
        "source": "World Bank",
        "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2023"],
        "values": [0.45, 0.55, 0.70, 0.87, 1.05, 1.23, 1.39, 1.43]
    },
    "gdp": {
        "title": "GDP (Current USD, Billions)",
        "source": "World Bank",
        "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2023"],
        "values": [37, 62, 186, 320, 468, 1675, 2667, 3549]
    },
    "life_expectancy": {
        "title": "Life Expectancy at Birth (Years)",
        "source": "World Bank",
        "labels": ["1960", "1970", "1980", "1990", "2000", "2010", "2020", "2022"],
        "values": [45.2, 48.7, 53.8, 58.6, 62.5, 66.8, 70.1, 72.0]
    }
}

world_data = {
    "comparisons": [
        {
            "id": "gdp",
            "name": "GDP (Trillion USD)",
            "source": "World Bank, 2023",
            "india": 3.5,
            "china": 17.7,
            "usa": 27.3,
            "world": 105.4
        },
        {
            "id": "population",
            "name": "Population (Billions)",
            "source": "World Bank, 2023",
            "india": 1.43,
            "china": 1.41,
            "usa": 0.33,
            "world": 8.02
        },
        {
            "id": "life_expectancy",
            "name": "Life Expectancy (Years)",
            "source": "World Bank, 2022",
            "india": 72.0,
            "china": 78.2,
            "usa": 76.3,
            "world": 71.3
        }
    ]
}

with open(os.path.join(DATA_DIR, "history.json"), "w", encoding="utf-8") as f:
    json.dump(history_data, f, indent=2)

with open(os.path.join(DATA_DIR, "world.json"), "w", encoding="utf-8") as f:
    json.dump(world_data, f, indent=2)

print("history.json and world.json generated successfully.")
