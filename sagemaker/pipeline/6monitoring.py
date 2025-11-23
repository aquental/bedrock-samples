import sagemaker

# Define the pipeline name to monitor
PIPELINE_NAME = "california-housing-preprocessing-pipeline"

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Get the SageMaker client from the session
sagemaker_client = sagemaker_session.sagemaker_client

# List pipeline executions sorted by creation time (newest first)
response = sagemaker_client.list_pipeline_executions(
    PipelineName=PIPELINE_NAME,
    SortBy='CreationTime',
    SortOrder='Descending'
)

# Extract the execution summaries from the response
executions = response['PipelineExecutionSummaries']

# Check if any executions exist
if not executions:
    print("No pipeline executions found")
else:
    # Get the latest execution (first item in the list)
    latest_execution = executions[0]

    # Extract execution details from the latest execution
    execution_arn = latest_execution['PipelineExecutionArn']
    status = latest_execution['PipelineExecutionStatus']
    start_time = latest_execution['StartTime']

    # Display basic execution information
    print(f"Latest Execution ARN: {execution_arn}")
    print(f"Status: {status}")
    print(f"Start Time: {start_time}")

    # TODO: Get detailed execution information using describe_pipeline_execution with execution_arn
    execution_details = sagemaker_client.describe_pipeline_execution(
        PipelineExecutionArn=execution_arn
    )

    # TODO: Check if the execution has completed by looking for 'LastModifiedTime' in execution_details, if it exists:
    if 'LastModifiedTime' in execution_details:
        # Extract the last modified time which serves as end time for completed executions
        end_time = execution_details['LastModifiedTime']
        # Calculate how long the pipeline took to run
        duration = end_time - start_time
        print(f"End Time: {end_time}")
        print(f"Duration: {duration}")
