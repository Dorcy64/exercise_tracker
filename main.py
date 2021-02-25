import requests
from datetime import datetime
from math import ceil
import os


# ------------------------------Nutrition-API-------------------------------------
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
Nutrition_Endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
SHEETY_PASSWORD = os.environ.get("SHEETY_PASSWORD")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": input("Tell me which exercise you did: "),
    "gender": "male",
    "height_cm": 193,
    "weight_kg": 136,
    "age": 18,
}

response = requests.post(url=Nutrition_Endpoint, json=parameters, headers=headers)
if response.status_code == 200:
    print("success fully got nutrition")
else:
    print(response.text)

exercises = response.json()["exercises"]

EXERCISES = []
DURATION = 0
CALORIES = 0

for x in exercises:
    EXERCISES.append(str(x["name"]).title())
    DURATION += ceil(int(x["duration_min"]))
    CALORIES += ceil(int(x["nf_calories"]))

# --------------------------------Sheety-API---------------------------------------
today = datetime.now()

SHEET_ENDPOINT = "https://api.sheety.co/b1fb79a138c84824ab1833a9e3d2aa22/myWorkouts/workouts"

SHEETY_HEADER = {"Content-Type": "application/json"}

sheet_parameters = \
    {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": ", ".join(EXERCISES),
            "duration": DURATION,
            "calories": CALORIES,
        }

    }


response = requests.post(url=SHEET_ENDPOINT,
                         json=sheet_parameters,
                         headers=SHEETY_HEADER,
                         auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
if response.status_code == 200:
    print('Updated Successfully')
else:
    print(response.text)
