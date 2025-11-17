import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.serverless import ServerlessInferenceConfig

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

# Attach to existing training job
estimator = SKLearn.attach(TRAINING_JOB_NAME)

# Configure serverless inference
serverless_config = ServerlessInferenceConfig(
    memory_size_in_mb=2048,  # Memory allocation
    max_concurrency=10       # Max concurrent requests
)

# TODO: Set a meaningful endpoint name for your model
ENDPOINT_NAME = "california-housing-estimator-dvosdjye"

try:
    # TODO: Deploy the estimator as a serverless endpoint asynchronously
    predictor = estimator.deploy(
        serverless_inference_config=serverless_config,
        endpoint_name=ENDPOINT_NAME,
        wait=False
    )
    # TODO: Use describe_endpoint() to get detailed information about the endpoint
    endpoint_description = sagemaker_session.sagemaker_client.describe_endpoint(
        EndpointName=ENDPOINT_NAME)
    # TODO: Extract the endpoint status from the response
    status = endpoint_description['EndpointStatus']
    # TODO: Print the endpoint status
    print(f"Endpoint status: {status}")
except Exception as e:
    print(f"Error: {e}")
