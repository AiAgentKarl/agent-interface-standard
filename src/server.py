"""Agent Interface Standard — Schema.org for AI Agents."""

from mcp.server.fastmcp import FastMCP
from src.tools.standard_tools import register_standard_tools

mcp = FastMCP(
    "Agent Interface Standard",
    instructions=(
        "The open standard for how businesses describe their services to AI agents. "
        "Like Schema.org made websites machine-readable for search engines, "
        "Agent Interface Standard makes businesses machine-readable for AI agents. "
        "Create, validate, register and discover agent-accessible business interfaces."
    ),
)

register_standard_tools(mcp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
