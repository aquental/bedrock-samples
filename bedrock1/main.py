import boto3

# Create a Bedrock Runtime client with your default region (us-east-1)
# client = boto3.client("bedrock-runtime", region_name="us-east-1")
client = boto3.client("bedrock-runtime", region_name="sa-east-1")

# Define a Bedrock model ID
# MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
MODEM_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

# Create the user message asking for AWS compute recommendations
messages = [
    {
        "role": "user",
        "content": [
            {
                "text": (
                    "Explain to a beginner what is AWS Bedrock."
                )
            }
        ],
    },
]

try:
    # Call Bedrock model using the converse method
    response = client.converse(
        modelId=MODEL_ID,
        messages=messages
    )

    # Get the output message from response
    output_message = response.get("output", {}).get("message", {})

    # Get the content parts from the message
    parts = output_message.get("content", [])

    # Extract text from each content part
    text_chunks = [part.get("text", "")
                   for part in parts if isinstance(part, dict)]

    # Join all text chunks into a single response
    full_response = "".join(text_chunks).strip()

    # Print the AI's response
    print(full_response)

except Exception as e:
    print(f"Error: {e}")
