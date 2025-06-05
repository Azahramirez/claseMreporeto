import streamlit as st 
import pandas as pd
from datetime import date
from utils.functions import load_data
from config import constants
from plotly import express as px
from plotly import graph_objects as go



# Set the tile and layout of the dashboard
st.title("Welcome to the BookML Dashboard! 📚🤖")
st.markdown("## Filter Panel for Hotel Occupancy Data")

table_names = constants.TABLE_NAMES
selected_table = st.selectbox("Select a table to view",
             options=table_names)

if selected_table == "ia_ocupaciones_gigante_limpia":
    df_ocupaciones = load_data(constants.DATASET_OCUPACIONES_LIMPIA, ["Fecha_hoy"])


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

elif selected_table == "ocupaciones_time_series_by_empresa":
    df_empresa = load_data(constants.DATASET_TS_BY_EMPRESA, ["Fecha_hoy"])
    unique_companies = df_empresa["ID_empresa"].unique()

    col1, col2  = st.columns(2)
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = date(2023, 1, 1)
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = date(2023, 12, 31)
    
    with col1:
        lower_date = st.date_input("Select the start date", value=df_empresa["Fecha_hoy"].min().date())
        upper_date = st.date_input("Select the end date", value=df_empresa["Fecha_hoy"].max().date())

        lower_date = pd.to_datetime(lower_date)
        upper_date = pd.to_datetime(upper_date)

    with col2:
        company = st.multiselect("Select the company", options=unique_companies, default=unique_companies[0])

    filtered_df = df_empresa[
        (df_empresa['ID_empresa'].isin(company)) &
        (df_empresa['Fecha_hoy'] >= lower_date) &
        (df_empresa['Fecha_hoy'] <= upper_date)
    ]

    total_num_men = filtered_df['num_men'].sum()
    total_num_adu = filtered_df['num_adu'].sum()
    total_trevpec = filtered_df['TREVPEC'].sum()
    total_ing_hab = filtered_df['ing_hab'].sum()


    st.markdown("### Summary Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        label="Total Number of Minors that Stayed",
        value=f"{int(total_num_men):,}"
    )
    with col2:
        st.metric(
        label="Total Number of Adults that Stayed",
        value=f"{int(total_num_adu):,}"
    )
    with col3:
        st.metric(
            label="Total Revenue Per Person",
            value=f"${total_trevpec:,.2f}",
        )
    if filtered_df.empty:
        st.warning("No results found for the selected filters.")

    st.subheader("Total Revenue Per Client Per Day:")
    # Making a time series plot group by date
    trevpec_df = filtered_df.groupby(['Fecha_hoy', 'ID_empresa']).agg({'TREVPEC': 'sum'}).reset_index()
    trevpec_fig = px.line(trevpec_df, x='Fecha_hoy', y='TREVPEC', color="ID_empresa",  title='TREVPEC Over Time By Company')
    st.plotly_chart(trevpec_fig, use_container_width=True)

    ing_hab_df = filtered_df.groupby(['Fecha_hoy', 'ID_empresa']).agg({'ing_hab': 'sum'}).reset_index()
    ing_hab_fig = px.line(ing_hab_df, x='Fecha_hoy', y='ing_hab', color="ID_empresa", title='Total Revenue Ing_hab Over Time By Company')
    st.plotly_chart(ing_hab_fig, use_container_width=True)


    cto_noc_df = (
    filtered_df
    .groupby(['Fecha_hoy', 'ID_empresa'], as_index=False)
    .agg({'cto_noc': 'mean'})  # or 'sum' if more appropriate
)

# Plot
    cto_noc_fig = px.line(
    cto_noc_df,
    x='Fecha_hoy',
    y='cto_noc',
    color='ID_empresa',
    title='Mean of Cost per Night (cto_noc) Over Time by Company'
)

    st.plotly_chart(cto_noc_fig, use_container_width=True)

elif selected_table == "ocupaciones_time_series_by_entidad":
    df_entidad = load_data(constants.DATASET_TS_BY_ENTIDAD, ["Fecha_hoy"])
    unique_states = df_entidad["ID_Entidad_Fed"].unique()

    col1, col2  = st.columns(2)
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = date(2023, 1, 1)
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = date(2023, 12, 31)

    with col1:
        lower_date = st.date_input("Select the start date", value=df_entidad["Fecha_hoy"].min().date())
        upper_date = st.date_input("Select the end date", value=df_entidad["Fecha_hoy"].max().date())

        lower_date = pd.to_datetime(lower_date)
        upper_date = pd.to_datetime(upper_date)

    with col2:
        state = st.multiselect("Select the state", options=unique_states, default=unique_states[0])

    filtered_df = df_entidad[
        (df_entidad['ID_Entidad_Fed'].isin(state)) &
        (df_entidad['Fecha_hoy'] >= lower_date) &
        (df_entidad['Fecha_hoy'] <= upper_date)
    ]


    total_num_people = filtered_df['num_adu'].sum() + filtered_df['num_men'].sum()
    total_trevpec = filtered_df['TREVPEC'].sum()

    mean_ocupation_rate = filtered_df['tasa_ocupacion'].mean()


    st.markdown("### Summary Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        label="Mean Occupation Rate (%)",
        value=f"{mean_ocupation_rate:,.2f} %")
    with col2:
        st.metric(
        label="Total Number of Poeple that Stayed",
        value=f"{int(total_num_people):,}")
    with col3:
        st.metric(
            label="Total Revenue Per Person",
            value=f"${total_trevpec:,.2f}",
        )
    if filtered_df.empty:
        st.warning("No results found for the selected filters.")
    

    st.subheader("Total Revenue Per Client Per State:")
    trevpec_df = filtered_df.groupby(['Fecha_hoy', 'ID_Entidad_Fed']).agg({'TREVPEC': 'sum'}).reset_index()
    trevpec_fig = px.line(trevpec_df, x='Fecha_hoy', y='TREVPEC', color="ID_Entidad_Fed", title='TREVPEC Over Time By State')
    st.plotly_chart(trevpec_fig, use_container_width=True)

    ing_hab_df = filtered_df.groupby(['Fecha_hoy', 'ID_Entidad_Fed']).agg({'ing_hab': 'sum'}).reset_index()
    ing_hab_fig = px.line(ing_hab_df, x='Fecha_hoy', y='ing_hab', color="ID_Entidad_Fed", title='Total Revenue Ing_hab Over Time By State')
    st.plotly_chart(ing_hab_fig, use_container_width=True)


    tasa_ocupacion_df = filtered_df.groupby(['Fecha_hoy', 'ID_Entidad_Fed']).agg({'tasa_ocupacion': 'mean'}).reset_index()
    tasa_ocupacion_fig = px.line(tasa_ocupacion_df, x='Fecha_hoy', y='tasa_ocupacion', color='ID_Entidad_Fed', title='Mean Occupation Rate Over Time by State')
    st.plotly_chart(tasa_ocupacion_fig, use_container_width=True)

elif selected_table == "reservaciones_time_series_by_room_type":
    df_room_type = load_data(constants.DATASET_TS_BY_ROOM_TYPE, ["fecha_ocupacion"])

    unique_types_room = df_room_type['ID_Tipo_Habitacion'].unique()



    col1, col2  = st.columns(2)
    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = date(2023, 1, 1)
    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = date(2023, 12, 31)

    with col1:
        lower_date = st.date_input("Select the start date", value=df_room_type["fecha_ocupacion"].min().date())
        upper_date = st.date_input("Select the end date", value=df_room_type["fecha_ocupacion"].max().date())

        lower_date = pd.to_datetime(lower_date)
        upper_date = pd.to_datetime(upper_date)

    with col2:
        room_type = st.multiselect("Select the room type", options=unique_types_room, default=unique_types_room[0])

    filtered_df = df_room_type[
        (df_room_type['ID_Tipo_Habitacion'].isin(room_type)) &
        (df_room_type['fecha_ocupacion'] >= lower_date) &
        (df_room_type['fecha_ocupacion'] <= upper_date)
    ]

    mean_ocupation_rate = filtered_df['tasa_ocupacion'].mean()
    h_num_noc = filtered_df['h_num_noc'].mean()
    h_num_per = filtered_df['h_num_per'].mean()


    st.markdown("### Summary Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
        label="Mean Occupation Rate (%)",
        value=f"{mean_ocupation_rate:,.2f} %")
    with col2:
        st.metric(
        label="Mean Number of Nights per Reservation",
        value=f"{h_num_noc:,.2f}")
    with col3:
        st.metric(
            label="Mean Number of People per Reservation",
            value=f"{h_num_per:,.2f}",
        )
    if filtered_df.empty:
        st.warning("No results found for the selected filters.")
    st.subheader("Mean Occupation Rate Per Room Type Per Day:")

    tasa_ocupacion_df = filtered_df.groupby(['fecha_ocupacion', 'ID_Tipo_Habitacion']).agg({'tasa_ocupacion': 'mean'}).reset_index()
    tasa_ocupacion_fig = px.line(tasa_ocupacion_df, x='fecha_ocupacion', y='tasa_ocupacion', color="ID_Tipo_Habitacion", title='Mean Occupation Rate Over Time By Room Type')
    st.plotly_chart(tasa_ocupacion_fig, use_container_width=True)

    h_num_noc_df = filtered_df.groupby(['fecha_ocupacion', 'ID_Tipo_Habitacion']).agg({'h_num_noc': 'mean'}).reset_index()
    h_num_noc_fig = px.line(h_num_noc_df, x='fecha_ocupacion', y='h_num_noc', color="ID_Tipo_Habitacion", title='Mean Number of Nights per Reservation Over Time By Room Type')
    st.plotly_chart(h_num_noc_fig, use_container_width=True)

    h_num_per_df = filtered_df.groupby(['fecha_ocupacion', 'ID_Tipo_Habitacion']).agg({'h_num_per': 'mean'}).reset_index()
    h_num_per_fig = px.line(h_num_per_df, x='fecha_ocupacion', y='h_num_per', color="ID_Tipo_Habitacion", title='Mean Number of People per Reservation Over Time By Room Type')
    st.plotly_chart(h_num_per_fig, use_container_width=True)

    



















    
















