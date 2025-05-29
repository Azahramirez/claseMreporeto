import streamlit as st 
from utils.functions import load_data
from config import constants
from plotly import express as px
from plotly import graph_objects as go




df_ocupaciones = load_data(constants.DATASET_OCUPACIONES_LIMPIA)

st.title("Welcome to the BookML Dashboard! 📚🤖")
st.subheader("Filter Panel")

unique_types_room = df_ocupaciones['ID_Tipo_Habitacion'].unique()
unique_states = df_ocupaciones['ID_Entidad_Fed'].unique()



col1, col2, col3 = st.columns(3)



with col1: 
     lower_date = st.date_input("Select the start date", value=st.session_state.get('start_date', None))
     upper_date = st.date_input("Select the end date", value=st.session_state.get('end_date', None))

with col2:
     type_room = st.selectbox("Select the type of room", options=unique_types_room, index=0)

with col3: 
     state = st.selectbox("Select the state of the reservation", options=unique_states, index=0)


filtered_df = df_ocupaciones[
    (df_ocupaciones['ID_Tipo_Habitacion'] == type_room) &
    (df_ocupaciones['ID_Entidad_Fed'] == state) &
    (df_ocupaciones['fecha_ocupacion'] >= lower_date) &
    (df_ocupaciones['fecha_ocupacion'] <= upper_date)
]









     
      





