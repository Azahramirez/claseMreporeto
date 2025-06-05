import streamlit as st 
import pandas as pd
from typing import List




@st.cache_data
def load_data(file_path:str, cols:List) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        cols (List): List of columns to convert to datetime.
        
    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    """
    # check extension of the file_path
    if file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
        for column in cols:
            data[column] = pd.to_datetime(data[column], errors='coerce')
            return data 
    elif file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
        for column in cols:
            data[column] = pd.to_datetime(data[column], errors='coerce')
        return data 
