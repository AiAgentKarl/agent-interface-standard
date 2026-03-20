# Agent Interface Standard 🌐

**Schema.org for AI Agents** — the open standard for how businesses describe their services to AI agents.

## The Vision

Schema.org made websites machine-readable for search engines. **Agent Interface Standard** makes businesses machine-readable for AI agents.

Businesses publish a simple JSON spec at `/.well-known/agent-interface.json` describing what services they offer and how agents can interact with them.

## Installation

```bash
pip install agent-interface-standard
```

```json
{"mcpServers": {"agent-interface": {"command": "uvx", "args": ["agent-interface-standard"]}}}
```

## Tools

| Tool | Description |
|------|-------------|
| `get_spec_template` | Get a blank template to fill out |
| `get_example_spec` | See a complete example (restaurant) |
| `validate_interface_spec` | Check your spec for errors |
| `register_business` | Register a business in the directory |
| `search_businesses` | Find agent-accessible businesses |
| `get_business_capabilities` | See what a business offers |
| `fetch_remote_spec` | Fetch a spec from a URL |

## The Spec Format

```json
{
  "agent_interface": "0.1.0",
  "business": {
    "name": "My Business",
    "description": "What we do",
    "category": "e_commerce"
  },
  "capabilities": [
    {
      "name": "search_products",
      "description": "Search our product catalog",
      "type": "search",
      "endpoint": "https://api.mybusiness.com/search",
      "method": "GET",
      "parameters": [...]
    }
  ],
  "auth": {"type": "api_key"},
  "pricing": {"model": "freemium"}
}
```

## Why This Matters

When AI agents become primary customers (not just humans), businesses need a standard way to be "agent-accessible." This is that standard.


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
