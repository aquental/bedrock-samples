import sagemaker
from sagemaker.model import ModelPackage
from sagemaker.serverless import ServerlessInferenceConfig

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Retrieve the AWS account ID for constructing resource ARNs
account_id = sagemaker_session.account_id()

# Define the SageMaker execution role
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# Define the model package group name where versioned models are stored
MODEL_PACKAGE_GROUP_NAME = "california-housing-pipeline-models"

# Name for the deployed SageMaker endpoint
ENDPOINT_NAME = "california-housing-estimator"

try:
    # Get the SageMaker client from the session
    sagemaker_client = sagemaker_session.sagemaker_client

    # List approved model packages from the group, sorted by creation time
    response = sagemaker_client.list_model_packages(
        ModelPackageGroupName=MODEL_PACKAGE_GROUP_NAME,
        ModelApprovalStatus='Approved',
        SortBy='CreationTime',
        SortOrder='Descending'
    )

    # Extract the model package list from the response
    model_packages = response.get('ModelPackageSummaryList', [])

    # Get the ARN of the latest approved model package
    model_package_arn = model_packages[0]['ModelPackageArn']

    # Create a ModelPackage object using the role, model_package_arn, and sagemaker_session
    model = ModelPackage(
        role=SAGEMAKER_ROLE,
        model_package_arn=model_package_arn,
        sagemaker_session=sagemaker_session
    )

    # Configure serverless inference with memory and concurrency limits
    serverless_config = ServerlessInferenceConfig(
        memory_size_in_mb=2048,
        max_concurrency=10
    )

    # Deploy the model as a serverless endpoint
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
