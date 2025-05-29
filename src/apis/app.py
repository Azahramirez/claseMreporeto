from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel
import mlflow

from apis.utils.classes_requests import ProphetOccupationRequest



app = FastAPI()

# On windows, you may need to use the localhost instead of 127.0.0.1
mlflow.set_tracking_uri("http://127.0.0.1:5000")



@app.post("/predict")
def predict(data: ProphetOccupationRequest):
    model = mlflow.pyfunc.load_model("models:/TR_ocupacion/3") 
    # model = joblib.load("../models/prophet_model.pkl")

    start_date = pd.to_datetime(data.start_date)
    end_date = pd.to_datetime(data.end_date)
    
    
    future_dates = pd.date_range(start=start_date, end=end_date, freq='D')


    df = pd.DataFrame({
        'ds': future_dates,
        'cap': [data.cap] * len(future_dates),  # Assuming cap is a constant for all dates
        'floor': [data.floor] * len(future_dates)  # Assuming floor is a constant for all dates
    })
    
    forecast = model.predict(df)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return (result.to_dict(orient='records'))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prophet Occupation Prediction API!"}





