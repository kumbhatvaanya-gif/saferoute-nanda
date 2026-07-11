# SafeRoute AI

## [Open SafeRoute AI](https://YOUR-RENDER-LINK.onrender.com)

> **Disaster-aware travel guidance built around the traveler, not just the hazard.**

---

## What It Does

SafeRoute AI helps travelers make safer decisions during natural disasters and severe weather.

It uses the traveler’s:

* Location
* Destination
* Transportation method
* Mobility requirements
* Family or medical needs

It then creates a personalized safety plan.

---

## How It Works

```text
Traveler enters location
          ↓
SafeRoute checks hazard information
          ↓
Risk level is calculated
          ↓
Travel recommendation is generated
          ↓
Personalized safety actions are provided
```

---

## Supported Hazards

| Hazard                | Example Guidance                |
| --------------------- | ------------------------------- |
| 🌧️ Heavy rain        | Change outdoor plans            |
| 🌊 Flooding           | Avoid low-lying routes          |
| 🌎 Earthquakes        | Avoid damaged infrastructure    |
| 🔥 Wildfires          | Move away from affected areas   |
| 🌋 Volcanoes and lava | Follow official exclusion zones |
| 🌪️ Severe storms     | Delay unsafe travel             |
| ❄️ Snow               | Check transport disruption      |
| 🪨 Landslides         | Avoid unstable routes           |

---

## Risk Levels

| Level       | Meaning                    | Recommendation                     |
| ----------- | -------------------------- | ---------------------------------- |
| 🟢 Low      | No major hazard detected   | Continue with awareness            |
| 🟡 Moderate | Travel may be disrupted    | Modify the itinerary               |
| 🟠 High     | Serious hazard nearby      | Delay or relocate                  |
| 🔴 Extreme  | Immediate danger may exist | Follow official emergency guidance |

---

## Personalized Guidance

SafeRoute AI can adjust recommendations for:

* Wheelchair users
* Travelers with limited mobility
* Elderly travelers
* Children
* Pets
* Medical equipment
* Drivers
* Pedestrians
* Public-transport users

---

## Example Questions

SafeRoute AI can help answer:

* Is it safe to travel there?
* Is there lava or volcanic activity nearby?
* Should I cancel my outdoor plans?
* Are earthquakes affecting my destination?
* Should I delay my trip?
* What areas should I avoid?
* What should a wheelchair user do differently?
* Can I still travel to the airport?

---

## API Endpoint

### Create a Safety Plan

```http
GET /plan
```

### Example Request

```text
https://YOUR-RENDER-LINK.onrender.com/plan?location=Naples%2C%20Italy&mobility=wheelchair&transport=car&needs=children,pets
```

### Parameters

| Parameter   | Example         | Description                     |
| ----------- | --------------- | ------------------------------- |
| `location`  | `Naples, Italy` | Current location or destination |
| `mobility`  | `wheelchair`    | Accessibility requirement       |
| `transport` | `car`           | Transportation method           |
| `needs`     | `children,pets` | Additional traveler needs       |

---

## Example Response

```json
{
  "location": "Naples, Italy",
  "assessment": {
    "risk_level": "moderate",
    "recommended_decision": "modify_trip",
    "summary": "Conditions may affect travel. Monitor official alerts and adjust the itinerary."
  },
  "personalized_actions": [
    "Confirm accessible transportation.",
    "Keep identification, water and medication ready.",
    "Check official alerts before travelling."
  ],
  "route_constraints": [],
  "source_status": {
    "weather": "not_connected",
    "earthquakes": "not_connected",
    "natural_events": "not_connected"
  },
  "limitations": [
    "The service does not guarantee that a route is safe.",
    "Official emergency instructions always take priority."
  ]
}
```

---

## Agent Instructions

```text
Ask for location and traveler needs
                ↓
Call the /plan endpoint
                ↓
Read the risk level
                ↓
Explain the most urgent action
                ↓
Present personalized guidance
                ↓
Remind the traveler to follow authorities
```

The agent must:

1. Ask for the traveler’s location.
2. Ask about transport and accessibility needs.
3. Call `/plan`.
4. State the risk level first.
5. Give the most important actions clearly.
6. Never guarantee that a route is safe.
7. Prioritize official emergency instructions.

---

## What SafeRoute AI Can Do

* Create personalized safety actions
* Recommend itinerary changes
* Highlight accessibility needs
* Organize hazard information
* Provide structured travel decisions
* Suggest areas that may require avoidance

---

## What SafeRoute AI Cannot Do

* Issue evacuation orders
* Guarantee route safety
* Contact emergency services
* Confirm every road closure
* Confirm shelter capacity
* Confirm hospital capacity
* Replace local authorities

---

## Data Sources

The complete version can use:

* Open-Meteo for weather
* USGS for earthquake information
* NASA EONET for natural events

The response should always show which sources are available.

---

## Safety Notice

> **SafeRoute AI is a decision-support tool. Official emergency authorities and evacuation instructions always take priority.**
