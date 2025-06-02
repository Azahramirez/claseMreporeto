import streamlit as st
import requests 



st.title("Welcome to the BookML Predictions Page! 📚🤖")

model_name = st.selectbox(
    "Select a model to make predictions",
    # Names that are with the mlflow registry

    options=["TR_ocupacion", "TOcupacion_Tocu","TOcupacion_NumAdu253", "TOcupacion_NumAdu173", "TOcupacion_NumAdu48", "TOcupacion_NumAdu5", "Inghab"])

url_fastapi = f"http://127.0.0.1:8000/predict/{model_name}"



st.markdown("## Model Prophet_model")
st.markdown("### Model Description")
st.markdown("""
This model is designed to forecast hotel occupancy rates using historical data. It employs the Prophet algorithm, which is particularly effective for time series forecasting, especially when dealing with seasonal effects and holidays.
""")

st.markdown("### Model Features")
start_date = st.date_input("Select the start date for predictions", value=st.session_state.get('start_date', None))
end_date = st.date_input("Select the end date for predictions", value=st.session_state.get('end_date', None))

if model_name in ["TR_ocupacion", "TOcupacion_Tocu"]:
    
    prediction = requests.post(
        url_fastapi,
        json={
            "start_date": str(start_date),
            "end_date": str(end_date)
        }
    )
else: 
    prediction = requests.post(
        url_fastapi,
        json={
            "start_date": str(start_date),
            "end_date": str(end_date),
            "cap": 10000000000,  # Optional, default to 1.0
            "floor": 0.0  # Optional, default to 0.0
        }
    )



if prediction.status_code == 200:
    prediction_data = prediction.json()
    st.write("Predicted Occupancy Rates:")
    st.dataframe(prediction_data)
    
elif prediction.status_code == 400:
    st.error("Invalid input data. Please check the date range and try again.")



