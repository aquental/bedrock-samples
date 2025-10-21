import boto3

# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime")

# Define the model ID
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Define the system prompt that sets the AI's role and behavior
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."

# Create the user message asking about AWS services
messages = [
    {
        "role": "user",
        "content": [
            {
                "text": (
                    "Explain the key differences between Amazon ECS and EKS for container orchestration."
                )
            }
        ],
    },
]

# TODO: Configure conservative settings - use low temperature (0.1) and moderate top-p (0.7) for predictable responses
conservative_config = {
    "maxTokens": 256,
    # TODO: Set temperature for conservative responses
    "temperature": 0.1,
    # TODO: Set top-p for conservative responses
    "topP": 0.7,
}

# TODO: Configure balanced settings - use moderate temperature (0.3) and higher top-p (0.8) for balanced responses
balanced_config = {
    "maxTokens": 256,
    # TODO: Set temperature for balanced responses
    "temperature": 0.3,
    # TODO: Set top-p for balanced responses
    "topP": 0.8,
}

# TODO: Configure creative settings - use higher temperature (0.6) and high top-p (0.9) for creative responses
creative_config = {
    "maxTokens": 256,
    # TODO: Set temperature for creative responses
    "temperature": 0.6,
    # TODO: Set top-p for creative responses
    "topP": 0.9,
}

# Test all three configurations with the same query
configs = [
    ("Conservative", conservative_config),
    ("Balanced", balanced_config),
    ("Creative", creative_config)
]

for config_name, config in configs:
    print(f"\n=== {config_name} Configuration ===")
    print(f"Temperature: {config['temperature']}, Top-P: {config['topP']}")

    try:
        # Call Bedrock model with the current configuration
        response = client.converse(
            modelId=MODEL_ID,
            messages=messages,
            system=[{"text": system_prompt}],
            inferenceConfig=config,
        )

        # Extract and combine text content from the Bedrock response
        output_message = response.get("output", {}).get("message", {})
        parts = output_message.get("content", [])
        text_chunks = [part.get("text", "")
                       for part in parts if isinstance(part, dict)]
        full_response = "".join(text_chunks).strip()

        # Print the AI's response
        print(full_response)

    except Exception as e:
        print(f"Error with {config_name} configuration: {e}")
