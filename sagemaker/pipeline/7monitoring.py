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

    # Extract execution ARN
    execution_arn = latest_execution['PipelineExecutionArn']

    # Retrieve all steps for this specific execution
    steps_response = sagemaker_client.list_pipeline_execution_steps(
        PipelineExecutionArn=execution_arn
    )

    # Extract the steps from the response
    steps = steps_response['PipelineExecutionSteps']

    # Iterate through each step and display its details
    for step in steps:
        # Extract step information
        step_name = step['StepName']
        step_status = step['StepStatus']

        # Display step name and status
        print(f"\n{step_name}: {step_status}")

        # Extract the StartTime from the step using get() method with 'Not started' as default value
        start_time = step.get('StartTime', 'Not started')
        print(f"  Started: {start_time}")

        # Check if the step has started (StartTime is not 'Not started') and print the start time
        if 'StartTime' in step and 'EndTime' in step:
            step_end = step['EndTime']
            step_duration = step_end - step['StartTime']
            print(f"  Ended: {step_end}")
            print(f"  Duration: {step_duration}")

        # Check if the step has an 'EndTime' field (step has completed)
        if 'EndTime' in step:
            # Extract the step's end time
            step_end = step['EndTime']
            # Calculate step execution time
            step_duration = step_end - step['StartTime']
            print(f"Ended: {step_end}")
            print(f"Duration: {step_duration}")

        # Check if the step status is 'Failed' and if 'FailureReason' exists in the step
            # TODO: Print the failure reason to help with debugging
        if step_status == 'Failed' and 'FailureReason' in step:
            print(f"Failure Reason: {step['FailureReason']}")
