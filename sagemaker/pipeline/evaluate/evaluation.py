import os
import json
import tarfile
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

if __name__ == to "__main__":
    # Paths
    model_tar_path = "/opt/ml/processing/model/model.tar.gz"
    model_extract_path = "/opt/ml/processing/model"
    test_data_path = "/opt/ml/processing/test/test.csv"        # Fixed
    # Fixed (no trailing / needed)
    evaluation_dir = "/opt/ml/processing/evaluation"

    # Extract model
    print("Extracting model...")
    with tarfile.open(model_tar_path, "r:gz") as tar:
        tar.extractall(path=model_extract_path)

    # Load model (assuming train.py saved it as model.joblib in the tar root)
    model_path = os.path.join(model_extract_path, "model.joblib")
    print(f"Loading model from {model_path}")
    model = joblib.load(model_path)

    # Load test data
    print(f"Loading test data from {test_data_path}")
    test_df = pd.read_csv(test_data_path)

    # Separate features and target
    X_test = test_df.drop(columns=["MedHouseVal"])
    y_test = test_df["MedHouseVal"]

    print(f"Evaluating model on {len(X_test)} test samples...")

    # Predictions and metrics
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Evaluation report
    evaluation_report = {
        "regression_metrics": {
            "mse": float(mse),
            "rmse": float(rmse),
            "mae": float(mae),
            "r2_score": float(r2)
        }
    }

    # Save report
    Path(evaluation_dir).mkdir(parents=True, exist_ok=True)
    report_path = os.path.join(evaluation_dir, "evaluation.json")

    with open(report_path, "w") as f:
        json.dump(evaluation_report, f, indent=2)

    print(f"Evaluation complete! Report saved to {report_path}")
    print(f"MSE: {mse:.4f}, RMSE: {rmse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
