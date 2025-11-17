import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer
from sagemaker.predictor import Predictor

# Name of the deployed SageMaker endpoint to use for inference
ENDPOINT_NAME = "california-housing-local-model"

# Path to the test dataset CSV file
TEST_DATA_FILE = "data/california_housing_test.csv"

try:
    # Connect to the deployed SageMaker endpoint for inference
    predictor = Predictor(endpoint_name=ENDPOINT_NAME)

    # Set the serializer to convert input data to CSV format using CSVSerializer()
    predictor.serializer = CSVSerializer()

    # Set the deserializer to convert CSV responses back to Python objects using CSVDeserializer()
    predictor.deserializer = CSVDeserializer()

    # Load and split test data into features and target variable
    test_df = pd.read_csv(TEST_DATA_FILE)
    X_test = test_df.drop("MedHouseVal", axis=1)
    y_test = test_df["MedHouseVal"]

    # Make predictions on the test set using predictor.predict() with X_test.values
    predictions = predictor.predict(X_test.values)

    # Convert predictions to numpy array of floats
    predictions = np.array(predictions).astype(float).flatten()

    # Evaluate the model
    test_r2 = r2_score(y_test, predictions)
    test_rmse = np.sqrt(mean_squared_error(y_test, predictions))

    # Print the results
    print(f"R² Score: {test_r2:.4f}")
    print(f"RMSE: {test_rmse:.4f}")

except Exception as e:
    print(f"Error: {e}")
