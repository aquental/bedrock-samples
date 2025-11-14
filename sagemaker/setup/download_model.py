import tarfile
import joblib
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.s3 import S3Downloader

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# List most recent completed training job
training_jobs = sagemaker_session.sagemaker_client.list_training_jobs(
    SortBy='CreationTime',
    SortOrder='Descending',
    StatusEquals='Completed',
    NameContains='sagemaker-scikit-learn'
)

# Extract the name of the latest training job
TRAINING_JOB_NAME = training_jobs['TrainingJobSummaries'][0]['TrainingJobName']

# Attach to the latest completed training job
estimator = SKLearn.attach(TRAINING_JOB_NAME)

# Get model S3 location from the estimator
model_s3_uri = estimator.model_data

# Download the model artifact from S3
S3Downloader.download(model_s3_uri, ".")

# Extract model files from the downloaded tar.gz file
with tarfile.open("model.tar.gz", 'r:gz') as tar:
    tar.extractall(".")
