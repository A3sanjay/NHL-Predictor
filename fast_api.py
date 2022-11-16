from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
import numpy as np
import math

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    
    Points : int
    Wins : int
    PointsPercentage : float
    GoalsFor : int
    GoalsAgainst : int

knn_clf = pickle.load(open('regular_season_model.sav','rb'))


@app.post('/regular_season_prediction')
def regular_season_pred(input_parameters : model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    points = input_dictionary['Points']
    wins = input_dictionary['Wins']
    points_percentage = input_dictionary['PointsPercentage']
    goals_for = input_dictionary['GoalsFor']
    goals_against = input_dictionary['GoalsAgainst']


    input_list = [points, wins, points_percentage, goals_for, goals_against]
    data = np.array(input_list)
    prediction = math.trunc(knn_clf.predict(data.reshape(1, -1)).tolist()[0])
    
    return prediction
