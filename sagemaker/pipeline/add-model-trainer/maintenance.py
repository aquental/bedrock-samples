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
    framework_version="1.2-1",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    sagemaker_session=pipeline_session
)

# Define the processing step with inputs, outputs, and the script to run
processing_step = ProcessingStep(
    name="ProcessData",
    processor=processor,
    inputs=[
        sagemaker.processing.ProcessingInput(
            source=f"s3://{default_bucket}/datasets/california_housing.csv",
            destination="/opt/ml/processing/input"
        )
    ],
    outputs=[
        # Update the output_name to "training_dataset"
        sagemaker.processing.ProcessingOutput(
            output_name="training_dataset",
            source="/opt/ml/processing/training"
        ),
        sagemaker.processing.ProcessingOutput(
            output_name="test_data",
            source="/opt/ml/processing/test"
        )
    ],
    code="data_processing.py"
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

# Define the training step that uses output from the processing step
training_step = TrainingStep(
    name="TrainModel",
    estimator=estimator,
    inputs={
        # Update the output reference to match the new output name from the processing step
        "train": sagemaker.inputs.TrainingInput(
            s3_data=processing_step.properties.ProcessingOutputConfig.Outputs[
                "training_dataset"].S3Output.S3Uri
        )
    }
)

# Create pipeline by combining all steps
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
