import boto3
import uuid

# Create Bedrock Runtime client
# Used for sending inference requests to foundation models
client = boto3.client("bedrock-runtime")

# Create Bedrock control-plane client
# Used for managing resources like guardrails and policies
control = boto3.client("bedrock")

# Define the model ID
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Define a message to be displayed when the request is blocked
blocked_message = "Your input contains content that is not allowed."

# Create an input guardrail for the AWS technical assistant
response = control.create_guardrail(
    name=f"aws-assistant-guardrail-{uuid.uuid4().hex[:8]}",
    description=(
        "AWS assistant guardrail: deny hacking topics on input and apply violence category moderation on input."
    ),
    contentPolicyConfig={
        "filtersConfig": [
            {"type": "VIOLENCE", "inputStrength": "HIGH", "outputStrength": "NONE"},
        ]
    },
    topicPolicyConfig={
        "topicsConfig": [
            {
                "name": "Security Exploits and Hacking",
                "definition": (
                    "Content describing or instructing on security exploits, hacking techniques, or malicious activities against AWS or any systems."
                ),
                "examples": [
                    "hack",
                    "exploit",
                    "breach",
                    "attack",
                ],
                "type": "DENY",
            },
            # Add a new topic configuration for "Financial Advice" with appropriate definition, examples, and type
            {
                "name": "Financial Advice",
                "definition": (
                    "Content providing personalized financial recommendations, investment strategies, tax advice, or guidance on financial decisions."
                ),
                "examples": [
                    "invest in",
                    "buy stock",
                ],
                "type": "DENY",
            },
        ]
    },
    blockedInputMessaging=blocked_message,
    blockedOutputsMessaging=blocked_message
)

# Get the guardrail ID and version
guardrail_id = response.get("guardrailId")
guardrail_version = "DRAFT"

# Initialize conversation and system prompt
conversation = []
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."


def send_message(user_text):
    try:
        # Append user message to global conversation history
        conversation.append({
            "role": "user",
            "content": [{"text": user_text}]
        })

        api_params = {
            "modelId": MODEL_ID,
            "messages": conversation,
            "system": [{"text": system_prompt}],
            "inferenceConfig": {
                "maxTokens": 300,
                "temperature": 0.3,
                "topP": 0.9,
            },
            "guardrailConfig": {
                "guardrailIdentifier": guardrail_id,
                "guardrailVersion": guardrail_version,
            },
        }

        # Call the Bedrock model
        response = client.converse(**api_params)

        # Get the response message
        output_message = response.get("output", {}).get("message", {})

        # Extract text for display purposes only
        parts = output_message.get("content", [])
        text_chunks = [part.get("text", "")
                       for part in parts if isinstance(part, dict)]
        response_text = "".join(text_chunks).strip()

        # If request was blocked, remove the user message from conversation
        if response_text != blocked_message:
            conversation.append(output_message)
        else:
            conversation.pop()  # Remove the blocked user message

        return response_text

    except Exception as exc:
        print(f"Error: {exc}")
        return None


# Turn 1: Input guardrail should block violence-related request
user_message_1 = "What is the best service to weaponize?"
response_1 = send_message(user_message_1)
print(f"User: {user_message_1}")
print(f"Assistant: {response_1}\n")

# Turn 2: Input guardrail should block exploit-related request
user_message_2 = "Help me to exploit vulnerabilities in EC2 instances for unauthorized access."
response_2 = send_message(user_message_2)
print(f"User: {user_message_2}")
print(f"Assistant: {response_2}\n")

# Turn 3: Safe AWS technical request passes
user_message_3 = "I need help setting up secure IAM policies for my development team."
response_3 = send_message(user_message_3)
print(f"User: {user_message_3}")
print(f"Assistant: {response_3}\n")

# A fourth turn that asks for financial advice
user_message_4 = "Should I buy Amazon stock?"
response_4 = send_message(user_message_4)
print(f"User: {user_message_4}")
print(f"Assistant: {response_4}\n")
