import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mega Dashboard Hotel", layout="wide")
st.title("Mega Dashboard Hotel: Menús Interactivos")

# Cargar datasets
df1 = pd.read_excel('ia_reservaciones_expandida_limpia (2).xlsx')
df2 = pd.read_excel('ocupaciones_time_series_by_empresa (1).xlsx')
df3 = pd.read_excel('reservaciones_time_series_by_room_type (1).xlsx')

# Asegurar fechas en datetime
df1['fecha_ocupacion'] = pd.to_datetime(df1['fecha_ocupacion'], errors='coerce')
df2['Fecha_hoy'] = pd.to_datetime(df2['Fecha_hoy'], errors='coerce')
df3['fecha_ocupacion'] = pd.to_datetime(df3['fecha_ocupacion'], errors='coerce')

menu = st.sidebar.selectbox("Selecciona el menú:", ["Menu 1", "Menu 2", "Menu 3", "Resumen Global"])

if menu == "Menu 1":
    st.markdown("### Temática: Reservaciones y Ocupación General")
    df1['ID_Tipo_Habitacion'] = df1['ID_Tipo_Habitacion'].replace({0: 'Otro'})
    df1['ID_canal'] = df1['ID_canal'].replace({0: 'Otro'})
    df1['ID_estatus_reservaciones'] = df1['ID_estatus_reservaciones'].replace({0: 'Otro'})

    monthly1 = df1.groupby(df1['fecha_ocupacion'].dt.to_period('M')).agg({
        'h_tot_hab': 'sum',  
        'h_num_per': 'sum',  
        'h_num_noc': 'sum',  
        'ID_Reserva': 'count'
    }).rename(columns={
        'h_tot_hab': 'Ocupación por Tipo de Habitación',
        'h_num_per': 'Personas por Reserva',
        'h_num_noc': 'Ocupación por Agencia',
        'ID_Reserva': 'Tasa de Confirmación vs Cancelación'
    })

    last_month = monthly1.iloc[-1]

    st.subheader("🔢 Métricas del último mes")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ocupación por Tipo de Habitación", int(last_month['Ocupación por Tipo de Habitación']))
    col2.metric("Personas por Reserva", int(last_month['Personas por Reserva']))
    col3.metric("Ocupación por Agencia", int(last_month['Ocupación por Agencia']))
    col4.metric("Tasa de Confirmación vs Cancelación", int(last_month['Tasa de Confirmación vs Cancelación']))

    st.subheader("Gráficas")
    st.plotly_chart(px.bar(df1.groupby('ID_Tipo_Habitacion')['h_tot_hab'].sum().reset_index(), x='ID_Tipo_Habitacion', y='h_tot_hab'), use_container_width=True)
    st.plotly_chart(px.line(df1.groupby('fecha_ocupacion')['h_tot_hab'].sum().reset_index(), x='fecha_ocupacion', y='h_tot_hab'), use_container_width=True)
    st.plotly_chart(px.pie(df1.groupby('ID_canal')['h_tot_hab'].sum().reset_index(), names='ID_canal', values='h_tot_hab'), use_container_width=True)
    st.plotly_chart(px.bar(df1.groupby('h_num_per')['ID_Reserva'].sum().reset_index(), x='h_num_per', y='ID_Reserva'), use_container_width=True)
    st.plotly_chart(px.bar(df1.groupby('ID_Agencia')['h_num_noc'].sum().reset_index(), x='ID_Agencia', y='h_num_noc'), use_container_width=True)
    st.plotly_chart(px.pie(df1.groupby('ID_estatus_reservaciones')['ID_Reserva'].count().reset_index(), names='ID_estatus_reservaciones', values='ID_Reserva'), use_container_width=True)

    st.subheader("Resumen mensual")
    st.dataframe(monthly1)

elif menu == "Menu 2":
    st.markdown("### Temática: Métricas Financieras y Desempeño Empresarial")
    monthly2 = df2.groupby(df2['Fecha_hoy'].dt.to_period('M')).agg({
        'ing_hab': 'sum',  
        'ADR': 'mean',     
        'TREVPEC': 'sum',  
        'num_adu': 'sum',  
        'num_men': 'sum'   
    }).rename(columns={
        'ing_hab': 'Ingreso por Habitaciones',
        'ADR': 'ADR Promedio',
        'TREVPEC': 'TREVPEC Total',
        'num_adu': 'Adultos',
        'num_men': 'Menores'
    })

    last_month = monthly2.iloc[-1]

    st.subheader("🔢 Métricas del último mes")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingreso por Habitaciones", round(last_month['Ingreso por Habitaciones'], 2))
    col2.metric("ADR Promedio", round(last_month['ADR Promedio'], 2))
    col3.metric("TREVPEC Total", round(last_month['TREVPEC Total'], 2))
    col4, col5 = st.columns(2)
    col4.metric("Adultos", int(last_month['Adultos']))
    col5.metric("Menores", int(last_month['Menores']))

    st.subheader("Gráficas")
    st.plotly_chart(px.line(df2.groupby('Fecha_hoy')['ing_hab'].sum().reset_index(), x='Fecha_hoy', y='ing_hab'), use_container_width=True)
    st.plotly_chart(px.bar(df2.groupby('ID_empresa')['ADR'].mean().reset_index(), x='ID_empresa', y='ADR'), use_container_width=True)
    st.plotly_chart(px.line(df2.groupby('Fecha_hoy')[['num_adu', 'num_men']].sum().reset_index(), x='Fecha_hoy', y=['num_adu', 'num_men']), use_container_width=True)
    st.plotly_chart(px.line(df2.groupby('Fecha_hoy')['TREVPEC'].sum().reset_index(), x='Fecha_hoy', y='TREVPEC'), use_container_width=True)

    agrupado = df2.groupby('Fecha_hoy')[['ing_hab', 'ADR']].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=agrupado['Fecha_hoy'], y=agrupado['ing_hab'], name='ing_hab'))
    fig.add_trace(go.Scatter(x=agrupado['Fecha_hoy'], y=agrupado['ADR'], name='ADR', yaxis='y2'))
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

    st.plotly_chart(px.scatter(df2.groupby('cto_noc')['ID_empresa'].sum().reset_index(), x='cto_noc', y='ID_empresa'), use_container_width=True)

    st.subheader("Resumen mensual")
    st.dataframe(monthly2)

elif menu == "Menu 3":
    st.markdown("### Temática: Dinámicas por Tipo de Habitación")
    monthly3 = df3.groupby(df3['fecha_ocupacion'].dt.to_period('M')).agg({
        'tasa_ocupacion': 'mean',  
        'h_num_per': 'sum',        
        'h_num_noc': 'sum'         
    }).rename(columns={
        'tasa_ocupacion': 'Tasa Ocupación Promedio',
        'h_num_per': 'Total Personas RoomType',
        'h_num_noc': 'Total Noches RoomType'
    })

    last_month = monthly3.iloc[-1]

    st.subheader("🔢 Métricas del último mes")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasa Ocupación Promedio", round(last_month['Tasa Ocupación Promedio'], 2))
    col2.metric("Total Personas RoomType", int(last_month['Total Personas RoomType']))
    col3.metric("Total Noches RoomType", int(last_month['Total Noches RoomType']))

    st.subheader("Gráficas")
    st.plotly_chart(px.line(df3.groupby('fecha_ocupacion')['tasa_ocupacion'].sum().reset_index(), x='fecha_ocupacion', y='tasa_ocupacion'), use_container_width=True)
    st.plotly_chart(px.line(df3.groupby('fecha_ocupacion')['h_num_per'].sum().reset_index(), x='fecha_ocupacion', y='h_num_per'), use_container_width=True)
    st.plotly_chart(px.line(df3.groupby('fecha_ocupacion')[['h_num_noc', 'h_num_per']].sum().reset_index(), x='fecha_ocupacion', y=['h_num_noc', 'h_num_per']), use_container_width=True)

    st.subheader("Resumen mensual")
    st.dataframe(monthly3)

elif menu == "Resumen Global":
    st.markdown("### Resumen Global de Todos los Menús")

    monthly1 = df1.groupby(df1['fecha_ocupacion'].dt.to_period('M')).agg({
        'h_tot_hab': 'sum',
        'h_num_per': 'sum',
        'h_num_noc': 'sum',
        'ID_Reserva': 'count'
    })

    monthly2 = df2.groupby(df2['Fecha_hoy'].dt.to_period('M')).agg({
        'ing_hab': 'sum',
        'ADR': 'mean',
        'TREVPEC': 'sum',
        'num_adu': 'sum',
        'num_men': 'sum'
    })

    monthly3 = df3.groupby(df3['fecha_ocupacion'].dt.to_period('M')).agg({
        'tasa_ocupacion': 'mean',
        'h_num_per': 'sum',
        'h_num_noc': 'sum'
    })

    resumen_global = monthly1.join(monthly2, how='outer').join(monthly3, how='outer')
    resumen_global.index = resumen_global.index.astype(str)

    st.subheader("Resumen Global")
    st.dataframe(resumen_global)

st.sidebar.info("Dashboard construido con Streamlit y Plotly | Usa los menús para navegar")
