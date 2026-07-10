# SafeRoute Emergency Planner
SafeRoute converts a travel destination and traveler needs into a live hazard assessment, itinerary decision, personalized safety actions, and machine-readable route constraints.

Base URL: https://YOUR-RENDER-SERVICE.onrender.com

## GET /health
Returns service availability.

Example call:
```bash
curl "https://YOUR-RENDER-SERVICE.onrender.com/health"
```

Example response:
```json
{"ok":true,"service":"SafeRoute Emergency Planner"}
```

## GET /plan
Creates a disaster-aware travel action plan.

Required query parameter:
- `location`: Human-readable destination name.

Optional query parameters:
- `latitude` and `longitude`: Provide both to skip geocoding and improve reliability.
- `mobility`: `standard`, `wheelchair`, or `limited_mobility`.
- `transport`: `car`, `walking`, or `public_transit`.
- `needs`: Comma-separated values such as `children,elderly,pets,medical_equipment`.
- `horizon_days`: 1 to 7.
- `risk_radius_km`: 50 to 500.

Example call:
```bash
curl "https://YOUR-RENDER-SERVICE.onrender.com/plan?location=Los%20Angeles&latitude=34.0522&longitude=-118.2437&mobility=wheelchair&transport=car&needs=elderly,medical_equipment&horizon_days=3&risk_radius_km=300"
```

Example response:
```json
{
  "ok": true,
  "service": "SafeRoute Emergency Planner",
  "assessment": {
    "risk_score_0_to_100": 35,
    "risk_level": "moderate",
    "decision": "modify_itinerary"
  },
  "hazards": [],
  "personalized_actions": [],
  "route_constraints": [],
  "limitations": [
    "This is decision support, not an official warning, evacuation order, or guaranteed safe route."
  ]
}
```

## How an agent should use this service
1. Extract the destination, mobility needs, transport mode, and special needs from the user's request.
2. If coordinates are known, send both `latitude` and `longitude`; otherwise send only `location`.
3. Call `GET /plan` once with the relevant parameters.
4. Read `assessment.decision` first, then present the highest-scoring `hazards`.
5. Present `personalized_actions` and explain any itinerary change.
6. Pass `route_constraints` to a mapping or routing service when available.
7. Repeat the `limitations` and prioritize official emergency instructions.
8. If a source is unavailable, state that confidence is limited.
