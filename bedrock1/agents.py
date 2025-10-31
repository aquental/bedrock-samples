import os
from strands import Agent
from strands.models import BedrockModel

# Define the Bedrock model ID
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Read guardrail info from environment variables
GUARDRAIL_ID = os.getenv("GUARDRAIL_ID")
GUARDRAIL_VERSION = os.getenv("GUARDRAIL_VERSION", "DRAFT")

# Create a Bedrock model with guardrail configuration
model = BedrockModel(
    model_id=MODEL_ID,
    guardrail_id=GUARDRAIL_ID,
    guardrail_version=GUARDRAIL_VERSION
)

# Define the system prompt for AWS Technical Assistant
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."

# Create an agent with the Bedrock model and AWS Technical Assistant system prompt
agent = Agent(
    model=model,
    system_prompt=system_prompt
)

# Send your first message to the agent asking about AWS Bedrock
agent("Explain to a beginner what is AWS Bedrock.")

agent("Which models are available?")
