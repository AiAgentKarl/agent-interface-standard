"""Standard-Tools — Agent Interface Specs erstellen, validieren und nutzen."""

import json
import httpx
from datetime import datetime
from mcp.server.fastmcp import FastMCP

from src.schema import (
    SPEC_VERSION, EXAMPLE_SPEC, BUSINESS_TEMPLATE,
    CATEGORIES, CAPABILITY_TYPES, validate_spec, _get_db,
)


def register_standard_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_spec_template(category: str = "") -> dict:
        """Get a blank Agent Interface spec template for a business.

        Returns a template that businesses can fill out to make
        their services accessible to AI agents. Like Schema.org markup
        but for AI agents.

        Args:
            category: Business category for relevant examples (optional)
        """
        return {
            "spec_version": SPEC_VERSION,
            "template": BUSINESS_TEMPLATE,
            "available_categories": CATEGORIES,
            "capability_types": CAPABILITY_TYPES,
            "instructions": (
                "Fill out the template with your business details and capabilities. "
                "Each capability describes one action an AI agent can take. "
                "Use validate_spec to check your spec before publishing."
            ),
        }

    @mcp.tool()
    async def get_example_spec() -> dict:
        """Get a complete example Agent Interface spec.

        Shows a fully filled-out spec for a restaurant with
        menu browsing, ordering, and order tracking capabilities.
        Use this as a reference when creating your own spec.
        """
        return {
            "description": "Complete example spec for a restaurant business",
            "spec": EXAMPLE_SPEC,
            "note": "This shows all supported fields. Not all fields are required.",
        }

    @mcp.tool()
    async def validate_interface_spec(spec_json: str) -> dict:
        """Validate an Agent Interface spec for correctness.

        Checks that all required fields are present and properly formatted.
        Returns a list of errors if the spec is invalid.

        Args:
            spec_json: The spec as a JSON string
        """
        try:
            spec = json.loads(spec_json)
        except json.JSONDecodeError as e:
            return {"valid": False, "errors": [f"Invalid JSON: {e}"]}

        errors = validate_spec(spec)

        if errors:
            return {"valid": False, "errors": errors, "error_count": len(errors)}

        caps = spec.get("capabilities", [])
        return {
            "valid": True,
            "spec_version": spec.get("agent_interface", "unknown"),
            "business": spec.get("business", {}).get("name", ""),
            "capabilities_count": len(caps),
            "message": "Spec is valid and ready to publish.",
        }

    @mcp.tool()
    async def register_business(spec_json: str, business_id: str = "") -> dict:
        """Register a business interface spec in the local directory.

        Makes the business discoverable by agents through search_businesses.
        The spec is stored locally and persists between sessions.

        Args:
            spec_json: The complete Agent Interface spec as JSON
            business_id: Custom ID (auto-generated from business name if empty)
        """
        try:
            spec = json.loads(spec_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON: {e}"}

        errors = validate_spec(spec)
        if errors:
            return {"error": "Invalid spec", "errors": errors}

        business = spec.get("business", {})
        name = business.get("name", "Unknown")

        if not business_id:
            business_id = name.lower().replace(" ", "-").replace(".", "-")[:50]

        conn = _get_db()
        conn.execute("""
            INSERT OR REPLACE INTO interfaces
            (id, business_name, description, category, spec_json,
             capabilities_count, website, registered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            business_id, name, business.get("description", ""),
            business.get("category", ""),
            json.dumps(spec), len(spec.get("capabilities", [])),
            business.get("website", ""), datetime.utcnow().isoformat(),
        ))
        conn.commit()

        return {
            "status": "registered",
            "business_id": business_id,
            "name": name,
            "capabilities": len(spec.get("capabilities", [])),
        }

    @mcp.tool()
    async def search_businesses(query: str, category: str = "") -> dict:
        """Search for agent-accessible businesses.

        Find businesses that have published Agent Interface specs,
        making their services available to AI agents.

        Args:
            query: Search term (e.g. "restaurant", "booking", "delivery")
            category: Filter by category (optional)
        """
        conn = _get_db()
        q = f"%{query.lower()}%"

        if category:
            rows = conn.execute("""
                SELECT id, business_name, description, category, capabilities_count, website
                FROM interfaces
                WHERE (LOWER(business_name) LIKE ? OR LOWER(description) LIKE ?)
                  AND LOWER(category) LIKE ?
                ORDER BY business_name LIMIT 20
            """, (q, q, f"%{category.lower()}%")).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, business_name, description, category, capabilities_count, website
                FROM interfaces
                WHERE LOWER(business_name) LIKE ? OR LOWER(description) LIKE ?
                ORDER BY business_name LIMIT 20
            """, (q, q)).fetchall()

        results = [dict(r) for r in rows]
        return {"query": query, "results_count": len(results), "businesses": results}

    @mcp.tool()
    async def get_business_capabilities(business_id: str) -> dict:
        """Get all capabilities of a registered business.

        Returns the full spec including all available actions
        an agent can take with this business.

        Args:
            business_id: Business ID (from search_businesses)
        """
        conn = _get_db()
        row = conn.execute(
            "SELECT * FROM interfaces WHERE id = ?", (business_id,)
        ).fetchone()

        if not row:
            return {"error": f"Business '{business_id}' not found"}

        spec = json.loads(row["spec_json"])
        return {
            "business_id": business_id,
            "business": spec.get("business", {}),
            "capabilities": spec.get("capabilities", []),
            "auth": spec.get("auth", {}),
            "pricing": spec.get("pricing", {}),
            "contact": spec.get("contact", {}),
        }

    @mcp.tool()
    async def fetch_remote_spec(url: str) -> dict:
        """Fetch an Agent Interface spec from a remote URL.

        Businesses can host their spec at a well-known URL
        (e.g. example.com/.well-known/agent-interface.json).
        This tool fetches and validates it.

        Args:
            url: URL to the Agent Interface spec JSON
        """
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            spec = resp.json()

        errors = validate_spec(spec)
        business = spec.get("business", {})

        return {
            "url": url,
            "valid": len(errors) == 0,
            "errors": errors if errors else None,
            "business_name": business.get("name", "Unknown"),
            "capabilities_count": len(spec.get("capabilities", [])),
            "spec": spec if len(errors) == 0 else None,
            "hint": "Use register_business to add this to your local directory." if not errors else None,
        }
