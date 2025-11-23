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

# Step 2: Model Training
# Create an estimator that defines how the model will be trained
estimator = SKLearn(
    entry_point="train.py",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=pipeline_session
)

# Create the training step that connects to the processing step output
# - Set the step name
# - Use the estimator we defined above
# - Configure inputs to use the "train_data" output from processing_step
# - The input key should be "train" and use sagemaker.inputs.TrainingInput
# - Reference the S3 URI using processing_step.properties.ProcessingOutputConfig.Outputs["train_data"].S3Output.S3Uri
training_step = TrainingStep(
    name="TrainModel",    # Unique name for this step in our pipeline
    estimator=estimator,  # Our estimator we defined above
    inputs={
        # Use the training data output from our processing step as input
        "train": sagemaker.inputs.TrainingInput(
            # Reference the S3 URI where our processing step saved the training data
            s3_data=processing_step.properties.ProcessingOutputConfig.Outputs[
                "train_data"].S3Output.S3Uri
        )
    }
)
# Add training_step to the steps list along with processing_step
pipeline = Pipeline(
    name=PIPELINE_NAME,
    steps=[processing_step, training_step],
    sagemaker_session=sagemaker_session
)

try:
    # Create or update pipeline (upsert = update if exists, create if not)
    pipeline.upsert(role_arn=SAGEMAKER_ROLE)

    # Start pipeline execution and get execution object for monitoring
    execution = pipeline.start()

    # Print the unique ARN identifier for this execution
    print(f"Pipeline execution ARN: {execution.arn}")

    # Get detailed information about the execution
    execution_details = execution.describe()

    # Display the current status of the pipeline execution
    print(f"Status: {execution_details['PipelineExecutionStatus']}")

except Exception as e:
    print(f"Error: {e}")
