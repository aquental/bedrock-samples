import sagemaker

# Create a SageMaker session to interact with AWS SageMaker services
sagemaker_session = sagemaker.Session()

try:
    # Get list of all endpoints from SageMaker
    endpoints_response = sagemaker_session.sagemaker_client.list_endpoints()

    # Extract the endpoints array from the response
    endpoints = endpoints_response['Endpoints']

    if endpoints:
        # Iterate through each endpoint and delete it along with its configuration
        for endpoint in endpoints:
            # Get endpoint name
            endpoint_name = endpoint['EndpointName']
            # Get endpoint details to retrieve the configuration name
            endpoint_details = sagemaker_session.describe_endpoint(
                endpoint_name)
            # Extract the endpoint configuration name
            config_name = endpoint_details['EndpointConfigName']
            # Delete the endpoint first using delete_endpoint()
            sagemaker_session.delete_endpoint(endpoint_name)
            # Print confirmation message for endpoint deletion
            print(endpoint_details['EndpointStatus'])
            # Delete the endpoint configuration using delete_endpoint_config()
            sagemaker_session.delete_endpoint_config(config_name)
            # Print confirmation message for configuration deletion
            print(f"Endpoint config '{config_name}' deleted successfully.\n")
    else:
        print("No endpoints found to clean up.")

except Exception as e:
    print(f"Error during cleanup: {e}")
