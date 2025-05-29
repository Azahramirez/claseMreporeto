from pydantic import BaseModel



class ProphetOccupationRequest(BaseModel):
    """
    Request model for Prophet consultation.
    """
    start_date: str
    end_date: str    
    cap : float = 1.0  # Optional, default to 1.0
    floor : float = 0.0  # Optional, default to 0.0




