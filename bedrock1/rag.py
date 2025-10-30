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
    # Create the query_embedding_request dictionary with inputText, dimensions, and normalize fields
    query_embedding_request = {
        "inputText": test_query,  # The query text to embed
        # Number of dimensions for the embedding vector
        "dimensions": EMBEDDING_DIMENSIONS,
        # Normalize the embedding vector (recommended for similarity search)
        "normalize": True,
    }

    # TODO: Get embedding from Bedrock using bedrock_runtime_client.invoke_model()
    query_response = bedrock_runtime_client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        body=json.dumps(query_embedding_request)
    )

    # TODO: Load the response body using json.loads()
    query_response_body = json.loads(query_response["body"].read())

    # Extract the embedding vector from the response
    query_embedding = [float(x) for x in query_response_body["embedding"]]

    # Search for similar vectors in S3 Vectors index
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

    # Test 2: Full RAG workflow using Bedrock Knowledge Base
    rag_queries = [
        "What is Nimbus Assist?",
        "In Nimbus Assist's RAG pipeline, what are the default retrieval parameters and which metadata filters are applied by default?",
        "What is Tech Company Inc.'s paid time off (PTO) policy?",
    ]

    # Process each test query through the full RAG pipeline
    for query in rag_queries:
        print(f"\nQuery: {query}")

        # Use Bedrock Knowledge Base for retrieval and generation
        response = bedrock_agent_runtime_client.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": (
                        f"arn:aws:bedrock:{REGION_NAME}::foundation-model/{GENERATION_MODEL_ID}"
                    ),
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 3
                        }
                    },
                    "generationConfiguration": {
                        "inferenceConfig": {
                            "textInferenceConfig": {
                                "maxTokens": 500,
                                "temperature": 0.1,
                            }
                        },
                    },
                },
            },
        )

        # Extract and display the generated answer
        answer = response["output"]["text"]
        print(f"Answer: {answer}")

        # Display source documents used for generation
        citations = response.get("citations", [])
        if citations:
            print("Sources:")
            for citation in citations:
                for ref in citation.get("retrievedReferences", []):
                    metadata = ref.get("metadata", {})
                    source_key = metadata.get(
                        "x-amz-bedrock-kb-source-uri", metadata.get("filename", "Unknown"))
                    print(f"  - {source_key}")
        else:
            print("Sources: (none returned)")

except Exception as e:
    print(f"Error: {e}")
