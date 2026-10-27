"""${env_name} client.

The served AgentEnv bundle takes OpenEnv's MCP actions, so this client is an
``MCPToolClient``. Reset to a task, call the bundle's tools, and end each turn
with ``end_turn``. Its result carries the next turn's prompt, or once ``done``
the task's reward:

    >>> async with ${client}(base_url="http://localhost:8000") as env:
    ...     await env.reset(split="all", index=0)
    ...     tools = await env.list_tools()
    ...     ended = await env.call_tool("end_turn", response="Done.")
    ...     print(ended["done"], ended["reward"])
"""

from openenv.core.mcp_client import MCPToolClient


class ${client}(MCPToolClient):
    """Client for the ${env_name} environment."""
