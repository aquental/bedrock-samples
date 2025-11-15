import sagemaker
from sagemaker.modules.train import ModelTrainer
from sagemaker.modules.configs import SourceCode, InputData, Compute, OutputDataConfig

# Initialize SageMaker session and get configuration
sagemaker_session = sagemaker.Session()
default_bucket = sagemaker_session.default_bucket()
account_id = sagemaker_session.boto_session.client(
    'sts').get_caller_identity()['Account']
region = sagemaker_session.boto_region_name

# Configuration constants
S3_TRAIN_DATA_URI = f"s3://{default_bucket}/datasets/california_housing_train.csv"
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"
MODEL_OUTPUT_PATH = f"s3://{default_bucket}/models/california-housing/"
INSTANCE_TYPE = "ml.m5.large"
INSTANCE_COUNT = 1
VOLUME_SIZE_GB = 30

# Define the scikit-learn training image URI
sklearn_image = sagemaker.image_uris.retrieve(
    framework="sklearn",         # Specify the ML framework (scikit-learn)
    region=region,               # AWS region for the image
    version="1.2-1",             # scikit-learn version to use
    py_version="py3",            # Python version for the container
    # Instance type for compatibility (required by image_uris.retrieve)
    instance_type=INSTANCE_TYPE
)

# Specify the source code configuration
source_code = SourceCode(
    # Directory containing the training script and any additional code
    source_dir=".",
    entry_script="train.py",  # The main script SageMaker will run for training
)

# Define the compute configuration for ModelTrainer
compute_config = Compute(
    instance_type=INSTANCE_TYPE,  # Type of EC2 instance to use for training
    instance_count=INSTANCE_COUNT,  # Number of instances to launch for the training job
    # Size (in GB) of the EBS volume attached to the instance
    volume_size_in_gb=VOLUME_SIZE_GB
)

# Define the output data configuration for ModelTrainer
output_config = OutputDataConfig(
    s3_output_path=MODEL_OUTPUT_PATH
)

# Initialize the ModelTrainer with correct parameters
model_trainer = ModelTrainer(
    # Docker image URI for the scikit-learn training container
    training_image=sklearn_image,
    # Source code configuration (directory and entry script)
    source_code=source_code,
    # Base name for the SageMaker training job
    base_job_name="sklearn-modeltrainer",
    role=SAGEMAKER_ROLE,                  # IAM role for SageMaker to access AWS resources
    # Compute configuration (instance type, count, volume size)
    compute=compute_config,
    # Output configuration (S3 path for model artifacts)
    output_data_config=output_config
)

# Define the input data configuration
input_data = [
    InputData(
        channel_name="train",     # Name of the input channel for training data
        data_source=S3_TRAIN_DATA_URI,  # S3 URI where the training data is stored
    )
]

try:
    # Call train() to start the training job asynchronously (does not block)
    model_trainer.train(input_data_config=input_data, wait=False)

    # Access the latest training job information using model_trainer._latest_training_job
    latest_job = model_trainer._latest_training_job

    # Print the training job name using the training_job_name attribute
    print(f"Training job name: {latest_job.training_job_name}")

    # Print the training job status using the training_job_status attribute
    print(f"Training job status: {latest_job.training_job_status}")
except Exception as e:
    print(f"Error: {e}")
