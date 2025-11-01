import os
import json
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator

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

# AWS resource specifications
aws_resource_specs = [
    {
        "resource": "Free Tier Limits",
        "limits": {
            "ec2_hours_per_month": 750,
            "s3_storage_gb": 5,
            "lambda_requests": 1000000,
            "rds_hours_per_month": 750
        }
    }
]

# TODO: Implement a custom tool that returns the aws_resource_specs as a JSON string


@tool
def get_aws_resource_specs() -> str:
    """
    Retrieves AWS technical specifications, conversion factors, and free tier limits.
    These are accurate technical specifications that don't change.

    Returns:
        str: JSON formatted string containing AWS resource specifications
    """
    return json.dumps(aws_resource_specs, indent=2)


# Create an agent with both calculator and AWS resource specs tools
agent = Agent(
    model=model,
    system_prompt=system_prompt,
    # Pass the custom tool to the agent
    tools=[calculator, get_aws_resource_specs]
)

# Send your first message to the agent asking about storage calculations
agent("What are the current AWS resource specifications for free tier?")
