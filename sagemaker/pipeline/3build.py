import sagemaker
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.pipeline_context import PipelineSession

# Create a SageMaker session for immediate operations
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

# Create a processor that will run our data preprocessing script
processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    sagemaker_session=pipeline_session
)

# Define the processing step with inputs, outputs, and the script to run
processing_step = ProcessingStep(
    name="ProcessData1",   # Unique name for this step in the pipeline
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
# Print configuration details to verify setup
print(f"Input source: {processing_step.inputs[0].source}")
print(f"Input destination: {processing_step.inputs[0].destination}")
print(f"Train output name: {processing_step.outputs[0].output_name}")
print(f"Train output source: {processing_step.outputs[0].source}")
print(f"Test output name: {processing_step.outputs[1].output_name}")
print(f"Test output source: {processing_step.outputs[1].source}")
print(f"Processing script: {processing_step.code}")
