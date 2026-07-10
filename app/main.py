import os

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

app = FastAPI(
    title="SafeRoute AI",
    version="1.0.0",
    description="Disaster-aware travel and evacuation decision support.",
)


@app.get("/", response_class=HTMLResponse)
def homepage() -> str:
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <title>SafeRoute AI</title>
        <style>
          body {
            max-width: 850px;
            margin: 60px auto;
            padding: 20px;
            font-family: Arial, sans-serif;
            line-height: 1.6;
          }
          a { margin-right: 18px; }
        </style>
      </head>
      <body>
        <h1>SafeRoute AI</h1>
        <p>
          Personalized disaster-aware travel and evacuation decision support.
        </p>
        <a href="/docs">Test API</a>
        <a href="/health">Health check</a>
        <a href="/skill.md">SKILL.md</a>
      </body>
    </html>
    """


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "service": "SafeRoute AI",
        "version": "1.0.0",
    }


@app.get("/plan")
def create_plan(
    location: str = Query(..., min_length=2),
    mobility: str = "standard",
    transport: str = "car",
    needs: str = "",
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

    return {
        "location": location,
        "assessment": {
            "risk_level": "unknown",
            "recommended_decision": "continue_with_awareness",
            "summary": (
                "Live disaster feeds are not connected in this basic version. "
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
    base_url = os.getenv(
        "RENDER_EXTERNAL_URL",
        "https://YOUR-RENDER-SERVICE.onrender.com",
    )

    return f"""# SafeRoute AI

> Disaster-aware travel and evacuation decision support.

## Base URL

`{base_url}`

## Health Check

`GET {base_url}/health`

## Create a Plan

`GET {base_url}/plan`

Example:

`{base_url}/plan?location=Naples&mobility=wheelchair&transport=car&needs=children,pets`

## Agent Instructions

1. Collect the traveller's location and accessibility needs.
2. Call `/plan`.
3. Explain the risk assessment and actions.
4. Never guarantee that a route is safe.
5. Follow official emergency authorities.
"""
