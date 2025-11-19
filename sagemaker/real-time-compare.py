import time
import numpy as np
import pandas as pd
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer
from sagemaker.predictor import Predictor

# Endpoint names for comparison
SERVERLESS_ENDPOINT_NAME = "california-housing-estimator"
REALTIME_ENDPOINT_NAME = "california-housing-realtime"

# Path to the test dataset CSV file
TEST_DATA_FILE = "data/california_housing_test.csv"

try:
    # Connect to both endpoints
    serverless_predictor = Predictor(endpoint_name=SERVERLESS_ENDPOINT_NAME)
    realtime_predictor = Predictor(endpoint_name=REALTIME_ENDPOINT_NAME)

    # Set serializers and deserializers for both predictors
    serverless_predictor.serializer = CSVSerializer()
    serverless_predictor.deserializer = CSVDeserializer()
    realtime_predictor.serializer = CSVSerializer()
    realtime_predictor.deserializer = CSVDeserializer()

    # Load test data
    test_df = pd.read_csv(TEST_DATA_FILE)
    X_test = test_df.drop("MedHouseVal", axis=1)

    # Take a small sample for timing comparison
    X_sample = X_test.head(10).values

    print("Performance Comparison: Serverless vs Real-Time Endpoints")
    print("=" * 60)

    # Test serverless endpoint timing
    start_time = time.time()
    serverless_predictions = serverless_predictor.predict(X_sample)
    serverless_time = time.time() - start_time

    # Test real-time endpoint timing
    start_time = time.time()
    realtime_predictions = realtime_predictor.predict(X_sample)
    realtime_time = time.time() - start_time

    # Display results
    print(f"Serverless Endpoint Response Time: {serverless_time:.4f} seconds")
    print(f"Real-Time Endpoint Response Time: {realtime_time:.4f} seconds")
    print(
        f"Performance Difference: {abs(serverless_time - realtime_time):.4f} seconds")

    if realtime_time < serverless_time:
        print(
            f"Real-time endpoint was {serverless_time/realtime_time:.2f}x faster")
    else:
        print(
            f"Serverless endpoint was {realtime_time/serverless_time:.2f}x faster")

except Exception as e:
    print(f"Error: {e}")
