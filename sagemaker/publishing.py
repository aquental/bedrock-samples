import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer
from sagemaker.predictor import Predictor

# Set the name of the deployed SageMaker endpoint to use for inference
ENDPOINT_NAME = "california-housing-modeltrainer"

# Path to the test dataset CSV file
TEST_DATA_FILE = "data/california_housing_test.csv"

try:
    # Connect to existing serverless endpoint
    predictor = Predictor(endpoint_name=ENDPOINT_NAME)

    # Configure serializers for scikit-learn model
    predictor.serializer = CSVSerializer()
    predictor.deserializer = CSVDeserializer()

    # Load test data
    test_df = pd.read_csv(TEST_DATA_FILE)
    X_test = test_df.drop("MedHouseVal", axis=1)  # Features only
    y_test = test_df["MedHouseVal"]               # Ground truth for evaluation

    # Make predictions on entire test set
    predictions = predictor.predict(X_test.values)

    # Evaluate the model performance
    test_r2 = r2_score(y_test, predictions)
    test_rmse = np.sqrt(mean_squared_error(y_test, predictions))

    # Print the results
    print(f"R² Score: {test_r2:.4f}")
    print(f"RMSE: {test_rmse:.4f}")

except Exception as e:
    print(f"Error: {e}")
