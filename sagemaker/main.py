import sagemaker
import pandas as pd

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Get the default SageMaker bucket name
default_bucket = sagemaker_session.default_bucket()

# S3 prefix where the data is stored
DATA_PREFIX = "datasets"

# Download the file from S3
# Use sagemaker_session.download_data() with these parameters:
# - path: "downloaded_data" (local directory to save the file)
# - bucket: default_bucket (the S3 bucket to download from)
# - key_prefix: f"{DATA_PREFIX}/california_housing_train.csv" (the S3 file path)
sagemaker_session.download_data(
    path="downloaded_data",  # Local directory where the file will be saved
    bucket=default_bucket,   # S3 bucket to download from
    # S3 object key (file path in bucket)
    key_prefix=f"{DATA_PREFIX}/california_housing_train.csv"
)
# Read the downloaded CSV file with pandas and display the first five rows
df = pd.read_csv("downloaded_data/california_housing_train.csv")
print(df.head())
