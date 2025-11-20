import json
import sagemaker

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

try:
    # Get list of all endpoints from SageMaker
    endpoints_response = sagemaker_session.sagemaker_client.list_endpoints()

    # Extract the endpoints array from the response
    endpoints = endpoints_response['Endpoints']

    for endpoint in endpoints:
        # Print the name and status of each endpoint
        print(f"- {endpoint['EndpointName']} ({endpoint['EndpointStatus']})")

        # Get the endpoint name from the endpoint object
        endpoint_name = endpoint['EndpointName']

        # Use describe_endpoint() to get endpoint details
        endpoint_details = sagemaker_session.describe_endpoint(endpoint_name)

        # Extract the EndpointConfigName from the endpoint details
        config_name = endpoint_details['EndpointConfigName']

        # Use describe_endpoint_config() to get the full configuration details
        config_details = sagemaker_session.sagemaker_client.describe_endpoint_config(
            EndpointConfigName=config_name
        )

        # Display the configuration details as formatted JSON using json.dumps()
        print(json.dumps(config_details, indent=2, default=str))

except Exception as e:
    print(f"Error: {e}")
