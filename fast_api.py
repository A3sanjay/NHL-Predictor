# from fastapi import FastAPI
# import uvicorn
# from pydantic import BaseModel
# import math
# import regular_season_model

# app = FastAPI()

# class request_body(BaseModel):
#     points : int
#     wins : int
#     points_percentage : float
#     goals_for : int
#     goals_against : int

# app.post('/predict')
# def predict(data : request_body):
#     test_data = [[
#             data.league_rank
#     ]]

#     class_idx = math.trunc(regular_season_model.knn_clf.predict(test_data.reshape(1, -1)).tolist()[0])
#     return {'class' : class_idx}


