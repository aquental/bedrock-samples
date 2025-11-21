import sagemaker

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Get the default SageMaker bucket name
default_bucket = sagemaker_session.default_bucket()

# Local file path
DATA_PATH = "data/california_housing.csv"

# S3 prefix (folder path within the bucket)
DATA_PREFIX = "datasets"

try:
    # TODO: Upload the dataset using the upload_data() method
    model_artifact_uri = sagemaker_session.upload_data(
        path=DATA_PATH,
        bucket=default_bucket,
        key_prefix=DATA_PREFIX
    )
    # TODO: Print a success message showing where the data was uploaded
    print(f"Model artifacts uploaded to: {model_artifact_uri}")

except Exception as e:
    print(f"Error: {e}")
