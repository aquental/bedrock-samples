import sagemaker
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.pipeline_context import PipelineSession

# Create a SageMaker session for immediate operations
sagemaker_session = sagemaker.Session()

# Create a pipeline session for pipeline components
pipeline_session = PipelineSession()

# Retrieve the AWS account ID for constructing resource ARNs
account_id = sagemaker_session.boto_session.client(
    'sts').get_caller_identity()['Account']

# Define the SageMaker execution role
SAGEMAKER_ROLE = f"arn:aws:iam::{account_id}:role/SageMakerDefaultExecution"

# Create an SKLearnProcessor with:
# - Framework version "1.2-1"
# - The execution role
# - Instance type "ml.m5.large"
# - Instance count 1
# - The pipeline session
processor = SKLearnProcessor(
    framework_version="1.2-1",    # Specify scikit-learn version
    role=SAGEMAKER_ROLE,          # IAM role with necessary permissions
    instance_type="ml.m5.large",  # Compute instance type for processing
    instance_count=1,             # Number of instances to use
    sagemaker_session=pipeline_session  # Use pipeline session for deferred execution
)

# Print processor configuration to verify setup
print(f"Processor role ARN: {processor.role}")
print(f"Processor instance type: {processor.instance_type}")
print(f"Processor instance count: {processor.instance_count}")
