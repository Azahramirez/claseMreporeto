from fastapi import FastAPI, HTTPException
import pickle 
from prophet import Prophet
from class_request import ForecastRequest
import pandas as pd
import datetime



model = pickle.load(open('../models/prophet_model.pkl', 'rb'))

app = FastAPI()


@app.post("/forecast")
def get_forecast(request: ForecastRequest):
    """
    Get forecast for the next request
    
    """
    try: 
        start_date = request.start_date
        end_date = request.end_date

        if end_date < start_date: 
            raise HTTPException(status_code=400, detail="End date must be greater than start date")
        
        future_dates = pd.date_range(start=start_date, end=end_date)
        future_df = pd.DataFrame(future_dates, columns=['ds'])
        forecast = model.predict(future_df)
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        return result.to_dict(orient='records')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




