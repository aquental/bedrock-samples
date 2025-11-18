import sagemaker
from sagemaker.sklearn.model import SKLearnModel
from sagemaker.serverless import ServerlessInferenceConfig

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Get account id from the current AWS session
account_id = sagemaker_session.boto_session.client(
    'sts').get_caller_identity()['Account']

# Define the SageMaker execution role ARN using the account id
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# List most recent completed training job
training_jobs = sagemaker_session.sagemaker_client.list_training_jobs(
    SortBy='CreationTime',                 # Sort jobs by creation time
    SortOrder='Descending',                # Newest jobs first
    StatusEquals='Completed',              # Only include completed jobs
    NameContains='sklearn-modeltrainer'    # Filter to ModelTrainer jobs
)

# Extract the name of the latest training job
TRAINING_JOB_NAME = training_jobs['TrainingJobSummaries'][0]['TrainingJobName']

# Set a unique name for the SageMaker endpoint to be created
ENDPOINT_NAME = "california-housing-modeltrainer-dvsoghcf-"

try:
    # Get training job details to find model artifacts location
    training_job_details = sagemaker_session.describe_training_job(
        TRAINING_JOB_NAME)
    model_data = training_job_details['ModelArtifacts']['S3ModelArtifacts']

    # Create a SKLearnModel with the inference script
    model = SKLearnModel(
        model_data=model_data,               # S3 location of trained model artifacts
        role=SAGEMAKER_ROLE,                 # IAM role for SageMaker
        entry_point='entry_point.py',        # Inference script
        framework_version='1.2-1',           # scikit-learn version
        py_version='py3',                    # Python version
        sagemaker_session=sagemaker_session  # SageMaker session
    )

    # Configure serverless inference
    serverless_config = ServerlessInferenceConfig(
        memory_size_in_mb=2048,
        max_concurrency=10
    )

    # Deploy the model as a serverless endpoint with the unique endpoint name
    predictor = model.deploy(
        serverless_inference_config=serverless_config,
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
