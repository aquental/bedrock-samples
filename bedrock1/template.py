import boto3

# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime")

# Define the model ID
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Initialize global conversation history and system prompt for prompt chaining
conversation = []
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."


def send_message(user_text):
    try:
        # Append user message to global conversation history
        conversation.append({
            "role": "user",
            "content": [{"text": user_text}]
        })

        # Prepare the API call parameters with global system prompt
        api_params = {
            "modelId": MODEL_ID,
            "messages": conversation,
            "system": [{"text": system_prompt}],
            "inferenceConfig": {
                "maxTokens": 300,
                "temperature": 0.3,
                "topP": 0.9,
            }
        }

        # Call the Bedrock model
        response = client.converse(**api_params)

        # Get the response message
        output_message = response.get("output", {}).get("message", {})

        # Directly add the assistant's response to conversation history for chaining
        conversation.append(output_message)

        # Extract text for display purposes only
        parts = output_message.get("content", [])
        text_chunks = [part.get("text", "")
                       for part in parts if isinstance(part, dict)]
        response_text = "".join(text_chunks).strip()

        return response_text

    except Exception as e:
        print(f"Error: {e}")
        return None


# Template 1: Parameterized prompt template for detailed service overview
# Uses {aws_service} variable for reusability across different AWS services
detailed_overview_template = (
    "Please provide a brief overview of {aws_service}. "
    "Include key features, use cases, pricing models, and target scenarios."
)

# Template 2: Parameterized prompt template for specific topic inquiry - chains with first response
# Uses {topic} variable for asking about different service aspects
specific_topic_template = (
    "Based on the overview you provided, can you give me more detailed information "
    "specifically about {topic}?"
)

# Set variables for template substitution
# TODO: Change this to a different AWS service (e.g., "Amazon Lambda", "Amazon S3", "Amazon EC2")
aws_service = "Amazon Bedrock"
# TODO: Change this to a different topic (e.g., "security best practices", "performance optimization", "integration patterns")
topic = "cost optimization strategies"

# Turn 1: Use parameterized template to generate detailed service overview prompt
user_message_1 = detailed_overview_template.format(aws_service=aws_service)
response_1 = send_message(user_message_1)
print(f"User: {user_message_1}")
print(f"Assistant: {response_1}\n")

# Turn 2: Chain prompts with parameterized follow-up about specific topic
# This demonstrates prompt chaining with two parameterized templates
user_message_2 = specific_topic_template.format(topic=topic)
response_2 = send_message(user_message_2)
print(f"User: {user_message_2}")
print(f"Assistant: {response_2}")
