from pydantic import BaseModel


class ForecastRequest(BaseModel):
    start_date: str
    end_date : str