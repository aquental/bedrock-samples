import os
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, retrieve

# Define the Bedrock model ID
model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Read guardrail info from environment variables
guardrail_id = os.getenv("GUARDRAIL_ID")
guardrail_version = os.getenv("GUARDRAIL_VERSION", "DRAFT")

# Read knowledge base and region from environment variables
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
REGION = os.getenv("AWS_REGION")

# Create a Bedrock model with guardrail configuration
model = BedrockModel(
    model_id=model_id,
    guardrail_id=guardrail_id,
    guardrail_version=guardrail_version
)

# Define the system prompt for AWS Technical Assistant
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."

# Create an agent with both calculator and retrieve tools
agent = Agent(
    model=model,
    system_prompt=system_prompt,
    tools=[calculator, retrieve]
)

# Add advanced search with custom parameters
results = agent.tool.retrieve(
    text="Nimbus Assist",
    numberOfResults=5,
    score=0.7,
    knowledgeBaseId=KNOWLEDGE_BASE_ID,
    region=REGION,
)
# Print the results, including the tool use ID, status, and content text.
print(f"[{results['toolUseId']}] Status: {results['status']}, Response:")
print(results['content'][0]['text'])
