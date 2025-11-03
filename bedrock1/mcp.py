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

# Define the MCP client for AWS documentation
stdio_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",   # Set the correct command
            # Set the correct args
            args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# Create an agent with MCP tools for AWS documentation access
with stdio_mcp_client:
    # Get the tools from the MCP server
    mcp_tools = stdio_mcp_client.list_tools_sync()
    for tool in mcp_tools:
        print(f"Tool: {tool.tool_name}, type: {tool.tool_type}")
        spec = tool.tool_spec
        print(spec["description"])
        print(spec["inputSchema"])
        print("-" * 10)

    # Create an agent with MCP tools
    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[mcp_tools]
    )

    # Send your first message to the agent asking about recent AWS features
    agent("What are the most recent AWS Bedrock features released in 2025?")
