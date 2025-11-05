#!/bin/zsh
# Configure your AgentCore project
agentcore configure --entrypoint main.py --name my_agent


# Launch server to AWS with agentcore CLI
agentcore launch \
  --env GUARDRAIL_ID=$GUARDRAIL_ID \
  --env KNOWLEDGE_BASE_ID=$KNOWLEDGE_BASE_ID

# Check the runtime status
agentcore status

# Invoke agent (uses default session)
agentcore invoke '{"prompt":"What is Amazon Bedrock?"}'


# Invoke agent with explicit 33-char session id (uses a separate session)
agentcore invoke '{"prompt":"What is Amazon Bedrock?"}' --session-id sess-20250829-ABCDEFGHJKLMNPQRSTU

# Follow-up within the same custom session (remembers context for this session)
agentcore invoke '{"prompt":"Tell me more"}' --session-id sess-20250829-ABCDEFGHJKLMNPQRSTU


# Follow-up within the same custom session (remembers context for this session)--
agentcore invoke '{"prompt":"What is Amazon Bedrock?"}'
agentcore invoke '{"prompt":"Tell me more"}'
