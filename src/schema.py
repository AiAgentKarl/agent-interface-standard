"""Agent Interface Schema — der offene Standard für agent-lesbare Business-Beschreibungen.

Definiert das JSON-Format das Unternehmen veröffentlichen können,
damit AI-Agents ihre Services automatisch verstehen und nutzen können.
Vergleichbar mit Schema.org für Suchmaschinen, aber für AI-Agents.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".agent-interface" / "registry.db"

# Die Standard-Spec Version
SPEC_VERSION = "0.1.0"

# Beispiel einer Agent Interface Spec
EXAMPLE_SPEC = {
    "agent_interface": SPEC_VERSION,
    "business": {
        "name": "Example Restaurant",
        "description": "Italian restaurant with delivery",
        "category": "food_delivery",
        "website": "https://example-restaurant.com",
        "location": {"city": "Berlin", "country": "DE"},
    },
    "capabilities": [
        {
            "name": "view_menu",
            "description": "Browse the restaurant menu",
            "type": "read",
            "endpoint": "https://api.example-restaurant.com/menu",
            "method": "GET",
            "parameters": [
                {"name": "category", "type": "string", "required": False,
                 "description": "Filter by category (pizza, pasta, salad)"}
            ],
            "returns": "List of menu items with prices",
            "auth_required": False,
            "rate_limit": "60/min",
        },
        {
            "name": "place_order",
            "description": "Place a delivery order",
            "type": "transaction",
            "endpoint": "https://api.example-restaurant.com/orders",
            "method": "POST",
            "parameters": [
                {"name": "items", "type": "array", "required": True,
                 "description": "List of item IDs and quantities"},
                {"name": "delivery_address", "type": "string", "required": True,
                 "description": "Full delivery address"},
                {"name": "payment_method", "type": "string", "required": True,
                 "description": "Payment method (card, cash, x402)"},
            ],
            "returns": "Order confirmation with estimated delivery time",
            "auth_required": True,
            "cost": {"currency": "EUR", "estimate": "10-30"},
            "confirmation_required": True,
        },
        {
            "name": "track_order",
            "description": "Track an existing order status",
            "type": "read",
            "endpoint": "https://api.example-restaurant.com/orders/{order_id}",
            "method": "GET",
            "parameters": [
                {"name": "order_id", "type": "string", "required": True,
                 "description": "The order ID from place_order"}
            ],
            "returns": "Order status and estimated delivery time",
            "auth_required": True,
        },
    ],
    "auth": {
        "type": "api_key",
        "header": "X-API-Key",
        "registration_url": "https://example-restaurant.com/developers",
    },
    "pricing": {
        "model": "per_transaction",
        "details": "Menu browsing is free. Orders are charged at menu prices.",
    },
    "contact": {
        "support_email": "api@example-restaurant.com",
        "docs_url": "https://docs.example-restaurant.com",
    },
}

# Template-Spezifikation die Unternehmen ausfüllen können
BUSINESS_TEMPLATE = {
    "agent_interface": SPEC_VERSION,
    "business": {
        "name": "",
        "description": "",
        "category": "",
        "website": "",
        "location": {"city": "", "country": ""},
    },
    "capabilities": [],
    "auth": {"type": "none"},
    "pricing": {"model": "free"},
    "contact": {},
}

# Bekannte Business-Kategorien
CATEGORIES = [
    "e_commerce", "food_delivery", "travel_booking", "financial_services",
    "healthcare", "real_estate", "transportation", "education",
    "entertainment", "professional_services", "saas", "marketplace",
    "government", "utilities", "insurance", "logistics",
]

# Capability-Typen
CAPABILITY_TYPES = [
    "read",          # Daten lesen (GET)
    "write",         # Daten schreiben (POST/PUT)
    "transaction",   # Kostenpflichtige Aktion
    "search",        # Suche
    "booking",       # Reservierung/Buchung
    "subscription",  # Abo-Verwaltung
    "notification",  # Benachrichtigungen
]


def _get_db():
    """Datenbank für registrierte Business-Interfaces."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS interfaces (
            id TEXT PRIMARY KEY,
            business_name TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT DEFAULT '',
            spec_json TEXT NOT NULL,
            capabilities_count INTEGER DEFAULT 0,
            website TEXT DEFAULT '',
            registered_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def validate_spec(spec: dict) -> list[str]:
    """Agent Interface Spec validieren. Gibt Liste von Fehlern zurück."""
    errors = []

    if "agent_interface" not in spec:
        errors.append("Missing 'agent_interface' version field")

    business = spec.get("business", {})
    if not business.get("name"):
        errors.append("Missing 'business.name'")
    if not business.get("description"):
        errors.append("Missing 'business.description'")

    capabilities = spec.get("capabilities", [])
    if not capabilities:
        errors.append("No capabilities defined — at least one required")

    for i, cap in enumerate(capabilities):
        if not cap.get("name"):
            errors.append(f"Capability {i}: missing 'name'")
        if not cap.get("description"):
            errors.append(f"Capability {i}: missing 'description'")
        if not cap.get("endpoint"):
            errors.append(f"Capability {i}: missing 'endpoint'")

    return errors
