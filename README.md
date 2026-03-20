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

## License

MIT
