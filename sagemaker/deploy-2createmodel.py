import sagemaker
from sagemaker.sklearn.model import SKLearnModel
from sagemaker.serverless import ServerlessInferenceConfig

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Get the default bucket
default_bucket = sagemaker_session.default_bucket()

# Get account id from the current AWS session
account_id = sagemaker_session.boto_session.client(
    'sts').get_caller_identity()['Account']

# S3 URI where the locally trained model artifact is stored
MODEL_ARTIFACTS_S3 = f"s3://{default_bucket}/models/local-trained/model.tar.gz"

# Define the SageMaker execution role ARN using the account id
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# Choose a unique name for your SageMaker endpoint
# Remember: endpoint names must be unique within your AWS account!
# If you run this code multiple times, change the name each time
ENDPOINT_NAME = "california-housing-local-model-sgljhgl"

try:
    # Create a SKLearnModel from local model artifacts
    model = SKLearnModel(
        model_data=MODEL_ARTIFACTS_S3,       # S3 location of model.tar.gz
        role=SAGEMAKER_ROLE,                 # IAM role for SageMaker
        entry_point='entry_point.py',        # Inference script
        framework_version='1.2-1',           # scikit-learn version
        py_version='py3',                    # Python version
        sagemaker_session=sagemaker_session  # SageMaker session
    )

    # Create a ServerlessInferenceConfig with memory_size_in_mb=2048 and max_concurrency=10
    serverless_config = ServerlessInferenceConfig(
        memory_size_in_mb=2048,
        max_concurrency=10
    )

    # Deploy the model using model.deploy() with serverless_inference_config, endpoint_name=ENDPOINT_NAME, and wait=False
    predictor = model.deploy(
        serverless_inference_config=serverless_config,
        endpoint_name=ENDPOINT_NAME,
        wait=False
    )
    # Use sagemaker_session.sagemaker_client.describe_endpoint() with EndpointName=ENDPOINT_NAME to get endpoint info
    endpoint_description = sagemaker_session.sagemaker_client.describe_endpoint(
        EndpointName=ENDPOINT_NAME)

    # Extract the 'EndpointStatus' from the endpoint description and print it
    status = endpoint_description['EndpointStatus']
    print(f"Endpoint status: {status}")

except Exception as e:
    print(f"Error: {e}")
