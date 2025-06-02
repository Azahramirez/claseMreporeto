import streamlit as st 
import pandas as pd
from datetime import date
from utils.functions import load_data
from config import constants
from plotly import express as px
from plotly import graph_objects as go

df_ocupaciones = load_data(constants.DATASET_OCUPACIONES_LIMPIA, ["Fecha_hoy"])

st.title("Welcome to the BookML Dashboard! 📚🤖")
st.markdown("## Filter Panel for Hotel Occupancy Data")

unique_types_room = df_ocupaciones['ID_Tipo_Habitacion'].unique()
unique_states = df_ocupaciones['ID_Entidad_Fed'].unique()

col1, col2, col3 = st.columns(3)

if 'start_date' not in st.session_state:
    st.session_state['start_date'] = date(2023, 1, 1)
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = date(2023, 12, 31)

with col1: 
     lower_date = st.date_input("Select the start date", value=df_ocupaciones["Fecha_hoy"].min().date())
     upper_date = st.date_input("Select the end date", value=df_ocupaciones["Fecha_hoy"].max().date())

     lower_date = pd.to_datetime(lower_date)
     upper_date = pd.to_datetime(upper_date)

with col2:
     type_room = st.multiselect("Select the type of room", options=unique_types_room, default=unique_types_room[0])

with col3: 
     state = st.multiselect("Select the state of the reservation", options=unique_states, default=unique_states[0])





filtered_df = df_ocupaciones[
    (df_ocupaciones['ID_Tipo_Habitacion'].isin(type_room)) &
    (df_ocupaciones['ID_Entidad_Fed'].isin(state)) &
    (df_ocupaciones['Fecha_hoy'] >= lower_date) &
    (df_ocupaciones['Fecha_hoy'] <= upper_date)
]    


total_rows = filtered_df.shape[0]
total_revenue = filtered_df['ing_hab'].sum()
total_revenue_person = filtered_df["TREVPEC"].sum()

st.markdown("### Summary Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Number of Records",
         value=f"{total_rows:,}")
    
with col2: 
    
    st.metric(
            label="Total Revenue",
               value=f"${total_revenue:,.2f}",
    )    

with col3: 
    st.metric(
        label="Total Revenue Per Person",
        value=f"${total_revenue_person:,.2f}",
    )


if filtered_df.empty:
    st.warning("No results found for the selected filters.")

st.subheader("Total Revenue Per Client Per Day:")
# Making a time series plot group by date
trevpec_df = filtered_df.groupby('Fecha_hoy').agg({'TREVPEC': 'sum'}).reset_index()
trevpec_fig = px.line(trevpec_df, x='Fecha_hoy', y='TREVPEC', title='TREVPEC Over Time')
st.plotly_chart(trevpec_fig, use_container_width=True)

# column Total Revenue Per Day
st.subheader("Total Revenue Per Day")
revenue = filtered_df.groupby('Fecha_hoy').agg({'ing_hab': 'sum'}).reset_index()
revenue_fig = px.line(revenue, x='Fecha_hoy', y='ing_hab', title='Total Revenue Per Day')
st.plotly_chart(revenue_fig, use_container_width=True)


# Count of Type of Room Per Day
st.subheader("Count of Type of Room Per Day")
room_count = filtered_df.groupby(['Fecha_hoy', 'ID_Tipo_Habitacion']).size().reset_index(name='count')
room_count_fig = px.bar(room_count, x='Fecha_hoy', y='count', color='ID_Tipo_Habitacion', title='Count of Type of Room Per Day')
st.plotly_chart(room_count_fig, use_container_width=True)










