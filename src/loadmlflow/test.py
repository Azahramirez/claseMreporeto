import pandas as pd
import numpy as np
import joblib
from prophet import Prophet
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.pyfunc
from mlflow.models.signature import infer_signature

class ProphetWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load(context.artifacts["model_path"])
    
    def predict(self, context, model_input):
        return self.model.predict(model_input)

def run_prophet_forecasting(
    dataset_path: str,
    date_col: str,
    target_col: str,
    registered_model_name: str,
    experiment_name: str,
    growth_type: str = "logistic",
    holidays_df: pd.DataFrame = None,
    forecast_cutoff: str = "2023-01-01"
):
    # ✅ MLflow setup
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment(experiment_name)

    # ✅ Load and clean data
    df = pd.read_excel(dataset_path).sort_values(date_col, ascending=True)
    df = df[[date_col, target_col]].rename(columns={date_col: 'ds', target_col: 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    df = df[df['ds'] < forecast_cutoff]
    df['cap'] = 1.0
    df['floor'] = 0.0

    # ✅ Train/test split
    split_index = int(len(df) * 0.8)
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]

    # ✅ Model
    model = Prophet(growth=growth_type, holidays=holidays_df)
    model.fit(train)

    # ✅ Prediction
    future = test[['ds']].copy()
    future['cap'] = 1.0
    future['floor'] = 0.0
    forecast = model.predict(future)

    # ✅ Metrics
    y_true = test['y'].values
    y_pred = forecast['yhat'].values
    residuals = y_true - y_pred
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    mape = np.mean(np.abs(residuals / y_true))
    r2 = r2_score(y_true, y_pred)

    # ✅ Save model
    joblib.dump(model, "prophet_model.pkl")

    # ✅ Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("growth", growth_type)
        mlflow.log_param("holiday_count", len(holidays_df) if holidays_df is not None else 0)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)
        mlflow.log_metric("r2_score", r2)

        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=ProphetWrapper(),
            artifacts={"model_path": "prophet_model.pkl"},
            registered_model_name=registered_model_name,
            signature=infer_signature(future, forecast)
        )

    print("\n✅ Forecasting complete.")

if __name__ == "__main__":

    params = params = {
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

    run_prophet_forecasting(
        dataset_path="data/reservaciones_time_series.xlsx"
        ,date_col="fecha_ocupacion",
          target_col="tasa_ocupacion",
          registered_model_name="TR_ocupacion",
          experiment_name="Prophet Occupation Forecasting Time Series Reservations",
            growth_type="logistic",
            holidays_df = pd.DataFrame(params['mexican_holidays']),
            forecast_cutoff="2023-01-01"
          ) 
    
