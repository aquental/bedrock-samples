import tarfile
import sagemaker

# Create a SageMaker session
session = sagemaker.Session()

# Get the default bucket
bucket = session.default_bucket()

# TODO: Create a tar.gz file named 'model.tar.gz' using tarfile.open() with mode 'w:gz'
# TODO: Add 'trained_model.joblib' to the tar archive
with tarfile.open('model.tar.gz', 'w:gz') as tar:
    tar.add('trained_model.joblib')
# TODO: Use session.upload_data() to upload 'model.tar.gz' with key_prefix='models/local-trained'
model_artifact_uri = sagemaker_session.upload_data(
    path='model.tar.gz',
    bucket=bucket,
    key_prefix='models/local-trained'
)
# TODO: Print the S3 URI returned from upload_data()
print(f"Model artifacts uploaded to: {model_artifact_uri}")
