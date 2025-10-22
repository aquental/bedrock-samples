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

# TODO: Create a third parameterized prompt template that builds on the previous responses
# This template should ask for implementation examples in a specific programming language
# Use curly braces {} for variables that will be substituted
language_topic_template = (
    "Could you provide an example "
    "implemented in the {language} programming language?"
)

# Set variables for template substitution
aws_service = "Amazon Bedrock"
topic = "cost optimization strategies"
language = "Python"

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
print(f"Assistant: {response_2}\n")

# TODO: Implement Turn 3 using your new parameterized template
# Format the template with appropriate variables and call send_message()
# Print both the user message and assistant response
user_message_3 = language_topic_template.format(language=language)
response_3 = send_message(user_message_2)
print(f"User: {user_message_3}")
print(f"Assistant: {response_3}\n")
