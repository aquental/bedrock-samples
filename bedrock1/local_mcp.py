import os
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# Define the Bedrock model ID
model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Read guardrail info from environment variables
guardrail_id = os.getenv("GUARDRAIL_ID")
guardrail_version = os.getenv("GUARDRAIL_VERSION", "DRAFT")

# Create a Bedrock model with guardrail configuration
model = BedrockModel(
    model_id=model_id,
    guardrail_id=guardrail_id,
    guardrail_version=guardrail_version
)

# Define the system prompt for AWS Technical Assistant
system_prompt = "You are an AWS Technical Assistant. Provide clear, accurate information about AWS services."

# TODO: Change the StdioServerParameters to connect to the local server
stdio_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="python",
            args=["local_mcp_server.py"]
        )
    )
)

# Create an agent with MCP tools for AWS documentation access
with stdio_mcp_client:
    # Get the tools from the MCP server
    mcp_tools = stdio_mcp_client.list_tools_sync()

    # Create an agent with MCP tools
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[mcp_tools]
    )

    # Send your first message to the agent asking about recent AWS features
    agent("Can you provide a breakdown of our users, clusters and instances? Also provide cost overview for weekly and monthly periods.")
