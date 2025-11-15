import tarfile
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import sagemaker
from sagemaker.s3 import S3Downloader

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# List most recent completed training job
training_jobs = sagemaker_session.sagemaker_client.list_training_jobs(
    SortBy='CreationTime',
    SortOrder='Descending',
    StatusEquals='Completed',
    NameContains='sklearn-modeltrainer'  # Filter for ModelTrainer jobs
)

# Extract the training job name from the first job summary in the list
TRAINING_JOB_NAME = training_jobs['TrainingJobSummaries'][0]['TrainingJobName']

# Path to test data
TEST_DATA_FILE = "data/california_housing_test.csv"

try:
    # Use sagemaker_session.describe_training_job() to get details about the selected training job by name
    training_job_details = sagemaker_session.describe_training_job(
        TRAINING_JOB_NAME)

    # Extract the model S3 URI from training_job_details using the ModelArtifacts and S3ModelArtifacts path
    model_s3_uri = training_job_details['ModelArtifacts']['S3ModelArtifacts']

    # Download the model artifact from S3 using SageMaker's S3Downloader
    S3Downloader.download(model_s3_uri, ".")

    # Extract model files from the downloaded tar.gz file
    with tarfile.open("model.tar.gz", 'r:gz') as tar:
        tar.extractall(".")

    # Load the trained model
    model = joblib.load("model.joblib")

    # Load test data
    test_df = pd.read_csv(TEST_DATA_FILE)
    X_test = test_df.drop("MedHouseVal", axis=1)
    y_test = test_df["MedHouseVal"]

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model's performance
    test_r2 = r2_score(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Print evaluation metrics
    print(f"R² Score: {test_r2:.4f}")
    print(f"RMSE: {test_rmse:.4f}")

except Exception as e:
    print(f"Error: {e}")
