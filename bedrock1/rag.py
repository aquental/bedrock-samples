import os
import json
import boto3

# Create AWS clients
s3_vectors_client = boto3.client("s3vectors")
bedrock_runtime_client = boto3.client("bedrock-runtime")
bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime")

# AWS region name
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# Knowledge Base ID
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

# S3 Vectors configuration
VECTOR_BUCKET_NAME = "bedrock-vector-bucket"
VECTOR_INDEX_NAME = "bedrock-vector-index"

# Set the embedding model ID to use
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"

# Set the number of dimensions for the embeddings
EMBEDDING_DIMENSIONS = 1024

# RAG generation model configuration
GENERATION_MODEL_ID = "amazon.nova-pro-v1:0"

try:
    # Test 1: Direct vector search using S3 Vectors
    test_query = "What is Nimbus Assist?"

    # Generate embedding for the test query
    query_embedding_request = {
        "inputText": test_query,             # The query text to embed
        "dimensions": EMBEDDING_DIMENSIONS,  # Number of dimensions for the embedding vector
        "normalize": True,                   # Normalize the embedding vector (recommended for similarity search)
    }

    # Get embedding from Bedrock for the query
    query_response = bedrock_runtime_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps(query_embedding_request)
    )

    # Load the response body
    query_response_body = json.loads(query_response["body"].read())

    # TODO: Extract the embedding vector from the response
    # Hint: Convert the embedding array to a list of floats
    query_embedding = [float(x) for x in query_response_body["embedding"]]

    # TODO: Search for similar vectors in S3 Vectors index
    search_response = s3_vectors_client.query_vectors(
        vectorBucketName=VECTOR_BUCKET_NAME,       # S3 Vectors bucket name
        indexName=VECTOR_INDEX_NAME,               # S3 Vectors index name
        queryVector={"float32": query_embedding},  # Query vector to search for
        topK=3,                                    # Number of top results to return
        returnDistance=True,                       # Include distance in response
    )
    # Display direct search results
    print(f"Direct search results for '{test_query}':")
    for i, result in enumerate(search_response.get("vectors", []), 1):
        distance = result.get("distance")
        if distance is not None:
            print(f"  {i}. Key: {result['key']}, Distance: {distance:.4f}")
        else:
            print(f"  {i}. Key: {result['key']}")

except Exception as e:
    print(f"Error: {e}")
