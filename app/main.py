import os
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse


app = FastAPI(
    title="SafeRoute AI",
    version="1.0.0",
    description="Disaster-aware travel and evacuation decision support.",
)

BASE_URL = os.getenv(
    "RENDER_EXTERNAL_URL",
    "https://saferoute-travel-agent.onrender.com",
)

SKILL_FILE = Path(__file__).resolve().parent.parent / "SKILL.md"


@app.get("/", response_class=HTMLResponse)
def homepage() -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0"
        >

        <title>SafeRoute AI</title>

        <style>
          body {{
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 24px;
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background: #f7f8fa;
            color: #111827;
          }}

          h1 {{
            font-size: 42px;
            margin-bottom: 8px;
          }}

          h2 {{
            margin-top: 0;
          }}

          .subtitle {{
            font-size: 19px;
            color: #4b5563;
          }}

          .links {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 28px 0;
          }}

          .button {{
            display: inline-block;
            padding: 11px 18px;
            border-radius: 8px;
            background: #111827;
            color: white;
            text-decoration: none;
          }}

          .button.secondary {{
            background: white;
            color: #111827;
            border: 1px solid #d1d5db;
          }}

          .card {{
            margin-top: 24px;
            padding: 24px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
          }}

          .flow {{
            padding: 18px;
            border-radius: 10px;
            background: #f3f4f6;
            font-family: monospace;
            white-space: pre-line;
          }}

          code {{
            word-break: break-word;
          }}
        </style>
      </head>

      <body>
        <h1>SafeRoute AI</h1>

        <p class="subtitle">
          Personalized disaster-aware travel and evacuation decision support.
        </p>

        <div class="links">
          <a class="button" href="/docs">Test API</a>
          <a class="button secondary" href="/health">Health Check</a>
          <a class="button secondary" href="/skill.md">SKILL.md</a>
        </div>

        <div class="card">
          <h2>How it works</h2>

          <div class="flow">
Traveler enters a location
        ↓
SafeRoute reads traveler needs
        ↓
A personalized plan is generated
        ↓
The traveler follows official guidance
          </div>
        </div>

        <div class="card">
          <h2>Try an example</h2>

          <p>
            This example creates a plan for a wheelchair user travelling
            with children and pets.
          </p>

          <a
            href="/plan?location=Naples&mobility=wheelchair&transport=car&needs=children%2Cpets"
          >
            Open Naples safety plan
          </a>
        </div>

        <div class="card">
          <h2>Important limitation</h2>

          <p>
            The current prototype creates personalized emergency guidance,
            but live disaster feeds are not connected yet.
          </p>

          <p>
            Official emergency instructions always take priority.
          </p>
        </div>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "service": "SafeRoute AI",
        "version": "1.0.0",
        "website": BASE_URL,
    }


@app.get("/plan")
def create_plan(
    location: str = Query(
        ...,
        min_length=2,
        description="Current location or travel destination",
    ),
    mobility: str = Query(
        "standard",
        description="Mobility or accessibility requirement",
    ),
    transport: str = Query(
        "car",
        description="Transportation method",
    ),
    needs: str = Query(
        "",
        description="Comma-separated needs such as children,pets,medical",
    ),
) -> dict:
    actions = [
        "Monitor official emergency alerts for the selected location.",
        "Keep identification, water, medication, and a charged phone available.",
        "Do not use any route that local authorities have closed.",
    ]

    mobility_lower = mobility.lower()
    needs_lower = needs.lower()

    if "wheelchair" in mobility_lower or "limited" in mobility_lower:
        actions.append(
            "Confirm step-free transportation and accessible shelter options."
        )

    if "medical" in needs_lower:
        actions.append(
            "Carry medication, backup power, and emergency medical contacts."
        )

    if "children" in needs_lower:
        actions.append(
            "Choose a family meeting point and keep emergency contacts available."
        )

    if "pets" in needs_lower:
        actions.append(
            "Confirm pet-friendly shelter and transportation options."
        )

    if "elderly" in needs_lower:
        actions.append(
            "Allow additional evacuation time and avoid long walking routes."
        )

    if transport.lower() == "walking":
        actions.append(
            "Avoid long exposed walking routes during severe conditions."
        )

    if transport.lower() == "public_transport":
        actions.append(
            "Check official public-transport disruptions before travelling."
        )

    return {
        "location": location,
        "assessment": {
            "risk_level": "unknown",
            "recommended_decision": "continue_with_awareness",
            "summary": (
                "Live disaster feeds are not connected in this prototype. "
                "Check official alerts before travelling."
            ),
        },
        "transport": transport,
        "mobility": mobility,
        "personalized_actions": actions,
        "route_constraints": [],
        "source_status": {
            "weather": "not_connected",
            "earthquakes": "not_connected",
            "natural_events": "not_connected",
        },
        "limitations": [
            "This service does not guarantee that any route is safe.",
            "Official emergency instructions always take priority.",
        ],
    }


@app.get("/skill.md", response_class=PlainTextResponse)
def skill_markdown() -> str:
    if not SKILL_FILE.exists():
        return (
            "# SafeRoute AI\n\n"
            "The SKILL.md file could not be found in the repository root."
        )

    return SKILL_FILE.read_text(encoding="utf-8")
