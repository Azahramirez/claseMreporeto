import pandas as pd
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import joblib
import datetime
import numpy as np
import mlflow
import mlflow.pyfunc
from mlflow.models.signature import infer_signature

# ✅ STEP 1: Define a custom MLflow wrapper for Prophet
class ProphetWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import joblib
        from prophet import Prophet
        self.model = joblib.load(context.artifacts["model_path"])

    def predict(self, context, model_input):
        return self.model.predict(model_input)

# ✅ MLflow setup
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Time Series Forecasting with Prophet: Tabla de Reservaciones")

# Optional: autolog params/metrics
mlflow.autolog(disable=True)  # we'll log manually

# ✅ Load data
print("Leyendo ..")
reservaciones = pd.read_excel("data/reservaciones_time_series.xlsx").sort_values("Fecha_hoy", ascending=True)
print("Leyendo .. Hecho")

# ✅ Format data
df = reservaciones[['fecha_ocupacion', 'tasa_ocupacion']]
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])
# Quitar valores atípicos
df= df[df['ds'] < '2023-01-01']
df['cap'] = 1.0
df['floor'] = 0.0

# ✅ Holidays and parameters
params = {
    'mexican_holidays': {
        'holiday': [
            'New Year\'s Day', 'Constitution Day', 'Benito Juárez Day',
            'Labor Day', 'Independence Day', 'Revolution Day',
            'Christmas Day1', 'ChristmasDay2', 'ChristmasDay3', 'Christmas Day4', 'ChristmasDay5', 'ChristmasDay6',
            'Christmas Day7', 'ChristmasDay8', 'ChristmasDay9', 'Christmas Day10', 'ChristmasDay11',
            'Day of the Dead', 'Holy Thursday', 'Good Friday'
        ],
        'ds': pd.to_datetime([
            '2024-01-01', '2024-02-05', '2024-03-18', '2024-05-01',
            '2024-09-16', '2024-11-18', '2024-12-21', '2024-12-22',
            '2024-12-23', '2024-12-24', '2024-12-25', '2024-12-26',
            '2024-12-27', '2024-12-28', '2024-12-29', '2024-12-30',
            '2024-12-31', '2024-11-02', '2024-03-28', '2024-03-29'
        ]),
        'lower_window': -2,
        'upper_window': 2
    },
    'growth': 'logistic'
}

# ✅ Split data
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

# ✅ Train model
model = Prophet(growth=params['growth'], holidays=pd.DataFrame(params['mexican_holidays']))
model.fit(train)

# ✅ Save model locally (required for MLflow)
joblib.dump(model, "prophet_model.pkl")

# ✅ Predict
future = test[['ds']].copy()
future['cap'] = 1.0
future['floor'] = 0.0
forecast = model.predict(future)

# ✅ Evaluate
y_true = test['y'].values
y_pred = forecast['yhat'].values
residuals = y_true - y_pred
rmse = mean_squared_error(y_true, y_pred)** 0.5
mean_absolute_percent_error = round(np.mean(abs(residuals / y_true)), 4)
r2_score_value = r2_score(y_true, y_pred)
print('R2 Score:', r2_score_value)

print('Root Mean Squared Error (RMSE):', rmse)
print('Mean Absolute Percent Error:', mean_absolute_percent_error)

# ✅ Log model and metrics to MLflow
with mlflow.start_run():

    mlflow.log_param("growth", params["growth"])
    mlflow.log_param("mexican_holidays_count", len(params["mexican_holidays"]["ds"]))
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mean_absolute_percent_error", mean_absolute_percent_error)
    mlflow.log_metric("r2_score", r2_score_value)

    # Log the model as a custom PythonModel
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=ProphetWrapper(),
        artifacts={"model_path": "prophet_model.pkl"},
        registered_model_name="TR_ocupacion",
        signature=infer_signature(future, forecast)
    )