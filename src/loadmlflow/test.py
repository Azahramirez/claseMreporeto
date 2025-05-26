import pandas as pd
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime
import joblib
import numpy as np


import mlflow

from mlflow.models import infer_signature

# Si mlflow esta corriendo en la nube hay que darle una url específica, en este caso solo corre en local

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Time Series Forecasting with Prophet: Tabla de Reservaciones")

# Agrega metricas, manda todos los datos a mlflow
mlflow.autolog()

print("Leyendo ..")
# Load the wine dataset
reservaciones = pd.read_excel("data/reservaciones_time_series.xlsx").sort_values(
    "fecha_ocupacion",
    ascending=True,
)
print("Leyendo .. Hecho")

# Load the model
model = joblib.load("models/prophet_model.pkl")


df = reservaciones[['fecha_ocupacion','tasa_ocupacion']]
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])
df['cap'] = 1.0  # upper bound
df['floor'] = 0.0  # optional lower bound (default is 0)


X = df[['ds', 'cap', 'floor']]
y = df['y']


params = {
    'mexican_holidays':{
        'holiday': [
            'New Year\'s Day', 'Constitution Day', 'Benito Juárez Day',
            'Labor Day', 'Independence Day', 'Revolution Day',
            'Christmas Day1', 'ChristmasDay2', 'ChristmasDay3', 'Christmas Day4', 'ChristmasDay5', 'ChristmasDay6',
            'Christmas Day7', 'ChristmasDay8', 'ChristmasDay9', 'Christmas Day10', 'ChristmasDay11',
            'Day of the Dead', 'Holy Thursday', 'Good Friday'
        ],
        'ds': pd.to_datetime([
            '2024-01-01',  # Año Nuevo
            '2024-02-05',  # Día de la Constitución (first Monday of Feb)
            '2024-03-18',  # Natalicio de Benito Juárez (observed)
            '2024-05-01',  # Día del Trabajo
            '2024-09-16',  # Día de la Independencia
            '2024-11-18',  # Día de la Revolución (observed)
            '2024-12-21',  # Navidad
            '2024-12-22',  # Navidad
            '2024-12-23',  # Navidad
            '2024-12-24',  # Navidad
            '2024-12-25',  # Navidad
            '2024-12-26',  # Navidad
            '2024-12-27',  # Navidad
            '2024-12-28',  # Navidad
            '2024-12-29',  # Navidad
            '2024-12-30',  # Navidad
            '2024-12-31',  # Navidad
            '2024-11-02',  # Día de Muertos
            '2024-03-28',  # Jueves Santo
            '2024-03-29',  # Viernes Santo
        ]),
        'lower_window': -2,
        'upper_window': 2
    },
    'growth':'logistic'
}


# Split the dataset into training and testing sets
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

# Generate the future dataframe for predictions
future = test[['ds']]  # Use the actual dates from your test set
future['cap'] = 1.0
future['floor'] = 0.0

# Make predictions
forecast = model.predict(future)


# Compare predicted 'yhat' to actual 'y'
y_true = test['y'].values
y_pred = forecast['yhat'].values

# Evaluate the model
residuals = y_true - y_pred
rmse = mean_squared_error(test['y'], y_pred)**0.5
mean_absolute_percent_error= round(np.mean(abs(residuals/test['y'])),len(residuals))
print('Root Mean Squared Error (RMSE):', rmse)
print('Mean Absolute Percent Error:',mean_absolute_percent_error)

# Log the model and metrics to MLflow

with mlflow.start_run():


    mlflow.log_param("mexican_holidays", params["mexican_holidays"])
    mlflow.log_param("growth", params["growth"])
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mean_absolute_percent_error", mean_absolute_percent_error)
   

    # Log the model
    mlflow.sklearn.log_model(model, "model", registered_model_name="TR_ocupacion", signature=infer_signature(train['ds'], train['y']))