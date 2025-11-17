from sagemaker.predictor import Predictor

# Name of the deployed SageMaker endpoint to connect to
ENDPOINT_NAME = "california-housing-local-model"

try:
    # Create a Predictor object using the endpoint_name parameter
    predictor = Predictor(endpoint_name=ENDPOINT_NAME)

    # Call the endpoint_context() method on the predictor to get the endpoint context
    context = predictor.endpoint_context()

    # Extract the properties attribute from the context object
    properties = context.properties

    # Print the properties to verify the endpoint connection
    print(properties)

except Exception as e:
    print(f"Error: {e}")
