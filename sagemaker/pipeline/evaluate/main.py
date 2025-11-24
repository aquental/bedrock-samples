import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.properties import PropertyFile

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Create a pipeline session for pipeline components
pipeline_session = PipelineSession()

# Retrieve the AWS account ID for constructing resource ARNs
account_id = sagemaker_session.account_id()

# Get the default S3 bucket
default_bucket = sagemaker_session.default_bucket()

# Define the SageMaker execution role
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# Set a name for the SageMaker Pipeline
PIPELINE_NAME = "california-housing-evaluation-pipeline"

# Step 1: Data Processing
processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    sagemaker_session=pipeline_session
)

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
        sagemaker.processing.ProcessingOutput(
            output_name="train_data",
            source="/opt/ml/processing/train"
        ),
        sagemaker.processing.ProcessingOutput(
            output_name="test_data",
            source="/opt/ml/processing/test"
        )
    ],
    code="data_processing.py"
)

# Step 2: Model Training
estimator = SKLearn(
    entry_point="train.py",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=pipeline_session
)

training_step = TrainingStep(
    name="TrainModel",
    estimator=estimator,
    inputs={
        "train": sagemaker.inputs.TrainingInput(
            s3_data=processing_step.properties.ProcessingOutputConfig.Outputs[
                "train_data"].S3Output.S3Uri
        )
    }
)

# Step 3: Model Evaluation

# Create a processor for running the evaluation script
evaluation_processor = SKLearnProcessor(
    framework_version="1.2-1",    # Specify scikit-learn version
    role=SAGEMAKER_ROLE,          # IAM role with necessary permissions
    instance_type="ml.m5.large",  # Compute instance type for processing
    instance_count=1,             # Number of instances to use
    sagemaker_session=pipeline_session
)

# Define property file for evaluation metrics
evaluation_report_property = PropertyFile(
    # Unique identifier for this property file within the pipeline
    name="EvaluationReport",
    # Must match the output_name in the evaluation step's ProcessingOutput
    output_name="evaluation",
    # Path to the JSON file within the evaluation output directory
    path="evaluation.json"
)

# Define the evaluation step that takes the trained model and test data as input
evaluation_step = ProcessingStep(
    name="EvaluateModel",            # Unique name for this step in the pipeline
    processor=evaluation_processor,  # The processor we defined above
    inputs=[
        # Model artifact from the training step
        sagemaker.processing.ProcessingInput(
            source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model"
        ),
        # Test data from the processing step
        sagemaker.processing.ProcessingInput(
            source=processing_step.properties.ProcessingOutputConfig.Outputs[
                "test_data"].S3Output.S3Uri,
            destination="/opt/ml/processing/test"
        )
    ],
    outputs=[
        # Where the evaluation report will be saved
        sagemaker.processing.ProcessingOutput(
            output_name="evaluation",               # Reference name for this output
            # Container path where script saves report
            source="/opt/ml/processing/evaluation"
        )
    ],
    code="evaluation.py",               # The Python script that performs the evaluation
    # Enable access to evaluation metrics in subsequent pipeline steps
    property_files=[evaluation_report_property]
)

# Include the evaluation step to the pipeline
pipeline = Pipeline(
    name=PIPELINE_NAME,
    steps=[processing_step, training_step, evaluation_step],
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
