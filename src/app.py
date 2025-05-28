import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mega Dashboard Hotel", layout="wide")

st.title("Mega Dashboard Hotel: Menús Interactivos")

menu = st.sidebar.selectbox("Selecciona el menú:", ["Menu 1", "Menu 2", "Menu 3"])

if menu == "Menu 1":
    st.markdown("### Temática: Reservaciones y Ocupación General")
    df = pd.read_excel('ia_reservaciones_expandida_limpia (2).xlsx')
    df['ID_Tipo_Habitacion'] = df['ID_Tipo_Habitacion'].replace({0: 'Otro'})
    df['ID_canal'] = df['ID_canal'].replace({0: 'Otro'})
    df['ID_estatus_reservaciones'] = df['ID_estatus_reservaciones'].replace({0: 'Otro'})

    st.subheader("Ocupación por Tipo de Habitación")
    fig = px.bar(df.groupby('ID_Tipo_Habitacion')['h_tot_hab'].sum().reset_index(), x='ID_Tipo_Habitacion', y='h_tot_hab')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Evolución Temporal")
    if pd.api.types.is_numeric_dtype(df['fecha_ocupacion']):
        df['fecha_ocupacion'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(df['fecha_ocupacion'], unit='D')
    fig = px.line(df.groupby('fecha_ocupacion')['h_tot_hab'].sum().reset_index(), x='fecha_ocupacion', y='h_tot_hab')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Participación por Canal")
    fig = px.pie(df.groupby('ID_canal')['h_tot_hab'].sum().reset_index(), names='ID_canal', values='h_tot_hab')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Personas por Reserva")
    fig = px.bar(df.groupby('h_num_per')['ID_Reserva'].sum().reset_index(), x='h_num_per', y='ID_Reserva')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Ocupación por Agencia")
    fig = px.bar(df.groupby('ID_Agencia')['h_num_noc'].sum().reset_index(), x='ID_Agencia', y='h_num_noc')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tasa de Confirmación vs Cancelación")
    fig = px.pie(df.groupby('ID_estatus_reservaciones')['ID_Reserva'].count().reset_index(), names='ID_estatus_reservaciones', values='ID_Reserva')
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Menu 2":
    st.markdown("### Temática: Métricas Financieras y Desempeño Empresarial")
    df = pd.read_excel('ocupaciones_time_series_by_empresa (1).xlsx')
    if pd.api.types.is_numeric_dtype(df['Fecha_hoy']):
        df['Fecha_hoy'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(df['Fecha_hoy'], unit='D')

    st.subheader("Ingreso por habitaciones a lo largo del tiempo")
    st.plotly_chart(px.line(df.groupby('Fecha_hoy')['ing_hab'].sum().reset_index(), x='Fecha_hoy', y='ing_hab'), use_container_width=True)

    st.subheader("ADR promedio por empresa")
    st.plotly_chart(px.bar(df.groupby('ID_empresa')['ADR'].mean().reset_index(), x='ID_empresa', y='ADR'), use_container_width=True)

    st.subheader("Distribución de huéspedes (adultos vs. menores)")
    st.plotly_chart(px.line(df.groupby('Fecha_hoy')[['num_adu', 'num_men']].sum().reset_index(), x='Fecha_hoy', y=['num_adu', 'num_men']), use_container_width=True)

    st.subheader("TREVPEC a lo largo del tiempo")
    st.plotly_chart(px.line(df.groupby('Fecha_hoy')['TREVPEC'].sum().reset_index(), x='Fecha_hoy', y='TREVPEC'), use_container_width=True)

    st.subheader("Comparación entre ingresos y ADR")
    agrupado = df.groupby('Fecha_hoy')[['ing_hab', 'ADR']].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=agrupado['Fecha_hoy'], y=agrupado['ing_hab'], name='ing_hab'))
    fig.add_trace(go.Scatter(x=agrupado['Fecha_hoy'], y=agrupado['ADR'], name='ADR', yaxis='y2'))
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Nights sold por empresa")
    st.plotly_chart(px.scatter(df.groupby('cto_noc')['ID_empresa'].sum().reset_index(), x='cto_noc', y='ID_empresa'), use_container_width=True)

elif menu == "Menu 3":
    st.markdown("### Temática: Dinámicas por Tipo de Habitación")
    df = pd.read_excel('reservaciones_time_series_by_room_type (1).xlsx')
    if pd.api.types.is_numeric_dtype(df['fecha_ocupacion']):
        df['fecha_ocupacion'] = pd.to_datetime('1899-12-30') + pd.to_timedelta(df['fecha_ocupacion'], unit='D')

    st.subheader("Evolución de la tasa de ocupación")
    st.plotly_chart(px.line(df.groupby('fecha_ocupacion')['tasa_ocupacion'].sum().reset_index(), x='fecha_ocupacion', y='tasa_ocupacion'), use_container_width=True)

    st.subheader("Número de personas hospedadas")
    st.plotly_chart(px.line(df.groupby('fecha_ocupacion')['h_num_per'].sum().reset_index(), x='fecha_ocupacion', y='h_num_per'), use_container_width=True)

    st.subheader("Relación noches/personas")
    st.plotly_chart(px.line(df.groupby('fecha_ocupacion')[['h_num_noc', 'h_num_per']].sum().reset_index(), x='fecha_ocupacion', y=['h_num_noc', 'h_num_per']), use_container_width=True)

st.sidebar.info("Dashboard construido con Streamlit y Plotly | Usa los menús para navegar")