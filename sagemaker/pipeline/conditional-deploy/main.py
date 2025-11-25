import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.step_collections import RegisterModel
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.functions import JsonGet
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.model import SKLearnModel

# Create a SageMaker session for pipeline management
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
PIPELINE_NAME = "california-housing-conditional-pipeline"

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
evaluation_processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=SAGEMAKER_ROLE,
    instance_type="ml.m5.large",
    instance_count=1,
    sagemaker_session=pipeline_session
)

# Define property file for evaluation metrics
evaluation_report_property = PropertyFile(
    name="EvaluationReport",
    output_name="evaluation",
    path="evaluation.json"
)

evaluation_step = ProcessingStep(
    name="EvaluateModel",
    processor=evaluation_processor,
    inputs=[
        sagemaker.processing.ProcessingInput(
            source=training_step.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model"
        ),
        sagemaker.processing.ProcessingInput(
            source=processing_step.properties.ProcessingOutputConfig.Outputs[
                "test_data"].S3Output.S3Uri,
            destination="/opt/ml/processing/test"
        )
    ],
    outputs=[
        sagemaker.processing.ProcessingOutput(
            output_name="evaluation",
            source="/opt/ml/processing/evaluation"
        )
    ],
    code="evaluation.py",
    property_files=[evaluation_report_property]
)

# Step 4: Conditional Model Registration with automatic approval

# Name for the SageMaker Model Package Group where versioned models will be stored
MODEL_PACKAGE_GROUP_NAME = "california-housing-pipeline-models"

# Create a serving model object with a minimal inference script
inference_model = SKLearnModel(
    role=SAGEMAKER_ROLE,
    model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
    entry_point="entry_point.py",
    framework_version="1.2-1",
    py_version="py3",
    sagemaker_session=pipeline_session
)

# Configure the model registration step
register_step = RegisterModel(
    name="RegisterModel",
    model=inference_model,
    content_types=["text/csv"],
    response_types=["text/csv"],
    inference_instances=["ml.m5.large"],
    transform_instances=["ml.m5.large"],
    model_package_group_name=MODEL_PACKAGE_GROUP_NAME,
    approval_status="Approved"
)

# Create a ConditionGreaterThanOrEqualTo condition that checks if the R-squared score is >= 0.6
# - Use JsonGet to extract the R-squared score from the evaluation step
# - Set the left parameter to JsonGet with:
# - step_name should reference the evaluation step's name
# - property_file should use the evaluation report property file
# - json_path should point to the R-squared score in the JSON structure ("regression_metrics.r2_score")
# - Set the right parameter to 0.6 (the minimum threshold)
condition_r2_threshold = ConditionGreaterThanOrEqualTo(
    left=JsonGet(
        step_name=evaluation_step.name,
        property_file=evaluation_report_property,
        json_path="regression_metrics.r2_score"
    ),
    right=0.6
)

# Create a ConditionStep that only executes registration when the condition is met
# - Set the name parameter to an appropriate step name
# - Set the conditions parameter to a list containing the condition you created above
# - Set the if_steps parameter to a list containing the registration step (executed when condition is True)
# - Set the else_steps parameter to an empty list (no action when condition is False)
condition_step = ConditionStep(
    name="CheckModelQuality",
    conditions=[condition_r2_threshold],
    if_steps=[register_step],
    else_steps=[]
)

# Replace register_step with condition_step in the pipeline steps list
pipeline = Pipeline(
    name=PIPELINE_NAME,
    steps=[processing_step, training_step, evaluation_step, condition_step],
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
