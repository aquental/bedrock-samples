import sagemaker
from sagemaker.sklearn.estimator import SKLearn

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# List most recent completed training job
training_jobs = sagemaker_session.sagemaker_client.list_training_jobs(
    SortBy='CreationTime',                 # Sort jobs by creation time
    SortOrder='Descending',                # Newest jobs first
    StatusEquals='Completed',              # Only include completed jobs
    # Filter to jobs containing 'sagemaker-scikit-learn' in name
    NameContains='sagemaker-scikit-learn'
)

# Extract the name of the latest training job of the list
TRAINING_JOB_NAME = training_jobs['TrainingJobSummaries'][0]['TrainingJobName']

# Use SKLearn.attach() to connect to the training job and store the result in an estimator variable
estimator = SKLearn.attach(TRAINING_JOB_NAME)

# Print the framework version
print(f"Framework Version: {estimator.framework_version}")
# Print the model data S3 location
print(f"Model Data S3 Location: {estimator.model_data}")
# Print the container image URI
print(f"Container Image URI: {estimator.image_uri}")
