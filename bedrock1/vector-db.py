import boto3

# Create S3 Vectors client
s3_vectors_client = boto3.client("s3vectors")

# Create a unique vector bucket name
VECTOR_BUCKET_NAME = "bedrock-vector-bucket"
VECTOR_INDEX_NAME = "bedrock-vector-index"
EMBEDDING_DIMENSIONS = 1024
# Create an S3 vector bucket for embeddings storage
try:
    # Create an S3 vector bucket for embeddings storage
    s3_vectors_client.create_vector_bucket(vectorBucketName=VECTOR_BUCKET_NAME)
    # Create a vector index
    s3_vectors_client.create_index(
        vectorBucketName=VECTOR_BUCKET_NAME,  # Name of the S3 vector bucket
        indexName=VECTOR_INDEX_NAME,          # Name for the new vector index
        dimension=EMBEDDING_DIMENSIONS,       # Number of dimensions for embeddings
        distanceMetric="cosine",              # Similarity metric to use
        dataType="float32",                   # Data type for the vectors
    )
    # List the vector indexes in the bucket
    indexes_response = s3_vectors_client.list_indexes(
        vectorBucketName=VECTOR_BUCKET_NAME
    )

    # Get the vector index ARN
    index_arn = indexes_response["indexes"][0]["indexArn"]

    # Print the vector index ARN
    print(f"Vector Index ARN: {index_arn}")

except Exception as e:
    print(f"Error: {e}")
    print("Vector bucket created successfully!")
