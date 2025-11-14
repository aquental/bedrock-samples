import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# Path to test data
TEST_DATA_FILE = "data/california_housing_test.csv"

try:
    # Load the trained model
    model = joblib.load("model.joblib")

    # Load test data from CSV using pd.read_csv() with TEST_DATA_FILE
    TEST_DATA_FILE = "data/california_housing_test.csv"
    test_df = pd.read_csv(TEST_DATA_FILE)

    # Separate features from target variable by dropping "MedHouseVal" column for X_test and keeping it for y_test
    X_test = test_df.drop("MedHouseVal", axis=1)
    y_test = test_df["MedHouseVal"]
    # Make predictions on X_test using the model's predict() method
    y_pred = model.predict(X_test)
    # Calculate R² score using r2_score() with y_test and y_pred
    test_r2 = r2_score(y_test, y_pred)
    # Calculate RMSE using np.sqrt() and mean_squared_error() with y_test and y_pred
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    # Print the evaluation metrics
    print(f"R² Score: {test_r2:.4f}")
    print(f"RMSE: {test_rmse:.4f}")
except Exception as e:
    print(f"Error: {e}")
