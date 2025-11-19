import sagemaker
from sagemaker.sklearn.estimator import SKLearn

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# List most recent completed training job
training_jobs = sagemaker_session.sagemaker_client.list_training_jobs(
    SortBy='CreationTime',                 # Sort jobs by creation time
    SortOrder='Descending',                # Newest jobs first
    StatusEquals='Completed',              # Only include completed jobs
    NameContains='sagemaker-scikit-learn'  # Filter to sklearn estimator jobs
)

# Extract the name of the latest training job of the list
TRAINING_JOB_NAME = training_jobs['TrainingJobSummaries'][0]['TrainingJobName']

# Unique name to assign to the deployed real-time endpoint
ENDPOINT_NAME = "california-housing-realtime-ruzngf"
# Change the instance type to "ml.m5.xlarge" for better performance
INSTANCE_TYPE = "ml.m5.xlarge"
# Change the instance count to 2 to handle higher traffic volumes
INSTANCE_COUNT = 2

try:
    # Attach to existing training job
    estimator = SKLearn.attach(TRAINING_JOB_NAME)

    # Deploy as real-time endpoint
    predictor = estimator.deploy(
        initial_instance_count=INSTANCE_COUNT,
        instance_type=INSTANCE_TYPE,
        endpoint_name=ENDPOINT_NAME,
        wait=False
    )

    # Retrieve detailed information about the specified SageMaker endpoint
    endpoint_description = sagemaker_session.sagemaker_client.describe_endpoint(
        EndpointName=ENDPOINT_NAME)

    # Extract the current status of the endpoint from the response
    status = endpoint_description['EndpointStatus']

    # Display the endpoint's status
    print(f"Endpoint status: {status}")

except Exception as e:
    print(f"Error: {e}")
