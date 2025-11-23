import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.sklearn.processing import SKLearnProcessor

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Create a pipeline session for pipeline components
pipeline_session = PipelineSession()

# Retrieve the AWS account ID for constructing resource ARNs
account_id = sagemaker_session.boto_session.client(
    'sts').get_caller_identity()['Account']

# Get the default S3 bucket
default_bucket = sagemaker_session.default_bucket()

# Define the SageMaker execution role
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# Set a name for the SageMaker Pipeline
PIPELINE_NAME = "california-housing-training-pipeline"

# Step 1: Data Processing
# Create a processor that will run our data preprocessing script
processor = SKLearnProcessor(
    framework_version="1.2-1",    # Specify scikit-learn version
    role=SAGEMAKER_ROLE,          # IAM role with necessary permissions
    instance_type="ml.m5.large",  # Compute instance type for processing
    instance_count=1,             # Number of instances to use
    sagemaker_session=pipeline_session
)

# Define the processing step with inputs, outputs, and the script to run
processing_step = ProcessingStep(
    name="ProcessData",   # Unique name for this step in the pipeline
    processor=processor,  # The processor we defined above
    inputs=[
        # Define where the raw data comes from (S3 location)
        sagemaker.processing.ProcessingInput(
            source=f"s3://{default_bucket}/datasets/california_housing.csv",
            # Where data will be mounted in container
            destination="/opt/ml/processing/input"
        )
    ],
    outputs=[
        # Define where processed training data will be saved
        sagemaker.processing.ProcessingOutput(
            output_name="train_data",               # Reference name for this output
            source="/opt/ml/processing/train"       # Container path where script saves data
        ),
        # Define where processed test data will be saved
        sagemaker.processing.ProcessingOutput(
            output_name="test_data",                # Reference name for this output
            source="/opt/ml/processing/test"        # Container path where script saves data
        )
    ],
    code="data_processing.py"  # The Python script that performs the processing
)

# Create the estimator that defines how the model will be trained
# - Set the entry point to the training script filename
# - Set the role to SAGEMAKER_ROLE
# - Set the instance type to "ml.m5.large"
# - Set the instance count to 1
# - Set the framework version to "1.2-1"
# - Set the python version to "py3"
# - Set the sagemaker session to pipeline_session
estimator = SKLearn(
    entry_point="train.py",             # Our training script
    role=SAGEMAKER_ROLE,                # IAM role with necessary permissions
    instance_type="ml.m5.large",        # Compute instance type for training
    instance_count=1,                   # Number of instances to use
    framework_version="1.2-1",          # Specify scikit-learn version
    py_version="py3",                   # Python version
    sagemaker_session=pipeline_session  # Use pipeline session for deferred execution
)

# Print estimator configuration details
print("Estimator Configuration:")
print(f"Entry Point Script: {estimator.entry_point}")
print(f"Role: {estimator.role}")
print(f"Instance Type: {estimator.instance_type}")
print(f"Instance Count: {estimator.instance_count}")
print(f"Framework Version: {estimator.framework_version}")
print(f"Python Version: {estimator.py_version}")
print(f"SageMaker Session: {type(estimator.sagemaker_session).__name__}")
