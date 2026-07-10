# SafeRoute AI

## Personalized Disaster-Aware Travel and Evacuation Intelligence

> **The Safety Decision Layer for Travelers and Autonomous Travel Agents**

---

### Skill Information

| Property                 | Value                                                               |
| ------------------------ | ------------------------------------------------------------------- |
| **Skill Name**           | SafeRoute AI                                                        |
| **Version**              | 1.1.0                                                               |
| **Skill Type**           | Emergency Travel Decision Support                                   |
| **Primary Domain**       | Disaster-Aware Travel and Evacuation Planning                       |
| **Category**             | Travel • Safety • Weather • Hazards • Accessibility • Routing       |
| **Compatible Ecosystem** | NANDA Town                                                          |
| **Invocation Type**      | On-demand API Service                                               |
| **Primary Consumers**    | Autonomous AI Agents, Travel Assistants, Emergency Planning Systems |
| **Decision Authority**   | Advisory Only — Never Replaces Official Emergency Instructions      |
| **Base URL**             | `{{BASE_URL}}`                                                      |

---

## Abstract

SafeRoute AI is a disaster-aware travel and evacuation intelligence service that helps autonomous agents turn live hazard information into clear, personalized decisions.

Instead of merely displaying weather or disaster data, SafeRoute AI evaluates how current conditions may affect a specific traveler, destination, transportation method, accessibility requirement, and travel plan.

It combines weather forecasts, earthquake activity, and active natural-event information to produce:

* A structured risk assessment
* A recommended travel decision
* Prioritized safety actions
* Personalized accessibility guidance
* Machine-readable areas to avoid
* Data-source availability
* Clear safety limitations

SafeRoute AI is designed for situations involving:

* Severe rain
* Flooding
* Earthquakes
* Wildfires
* Volcanic activity
* Lava-related events
* Storms
* Snow
* Damaging winds
* Landslides
* Other travel-disrupting hazards

SafeRoute AI does not issue official evacuation orders, dispatch emergency services, or guarantee that any route is safe.

It provides explainable decision support so an autonomous agent can help a traveler act using evidence rather than scattered alerts.

---

# Vision

Travel applications are excellent at answering ordinary questions:

* What is the fastest route?
* Which hotel is closest?
* How long will the drive take?
* What attractions are open?
* What is the cheapest transportation option?

During a natural disaster, those questions change.

A traveler instead needs to know:

* Is the destination still safe enough to visit?
* Is heavy rain likely to disrupt the itinerary?
* Is a volcano or lava-related event active nearby?
* Are recent earthquakes relevant to the route?
* Is flooding likely to block transportation?
* Should the traveler continue, modify, delay, relocate, evacuate, or shelter in place?
* What changes are necessary for a wheelchair user?
* What should a family with children or pets do?
* What precautions are needed for someone carrying medical equipment?

Traditional mapping and travel systems often optimize convenience.

Emergency decisions require a different objective:

> **Reduce exposure to danger while clearly communicating uncertainty.**

SafeRoute AI exists to provide this missing safety decision layer.

It is built on a simple principle:

> **A travel agent should not only know where a traveler can go. It should know when the plan must change.**

---

# Problem Statement

Natural-disaster information is fragmented across:

* Weather services
* Earthquake feeds
* Satellite-derived event databases
* Local emergency alerts
* Government websites
* Transportation systems
* Maps
* News sources

A traveler may receive several alerts yet still lack an actionable answer.

For example, a tourist planning to visit Naples may see information about rain, earthquakes, and volcanic activity.

The available information may be technically accurate, but the traveler still needs help deciding:

* Is the hazard close enough to matter?
* Is the event recent?
* How serious is it?
* Does it affect driving, walking, or public transportation?
* Should outdoor plans be replaced?
* Should the traveler delay the trip?
* Is extra assistance required because of mobility or medical needs?
* Which instructions are urgent and which are precautionary?

This creates four major problems.

## 1. Information Fragmentation

Hazard information is distributed across multiple services and formats.

Travelers and autonomous agents must manually combine information before understanding the situation.

---

## 2. Data Without Decisions

Most services report conditions.

They do not convert those conditions into personalized recommendations such as:

* Continue with awareness
* Modify the itinerary
* Delay the trip
* Relocate to another area
* Follow official evacuation guidance
* Shelter in place

---

## 3. Generic Safety Advice

A single recommendation is not appropriate for every traveler.

A wheelchair user, family with children, elderly traveler, person with medical equipment, solo driver, and public-transport passenger may require different actions during the same event.

---

## 4. False Certainty

Emergency conditions can change quickly.

Any system that claims a route is guaranteed safe creates dangerous confidence.

A responsible system must:

* Communicate uncertainty
* Report unavailable data
* Avoid guaranteeing safety
* Defer to official emergency authorities
* Clearly distinguish recommendations from official orders

SafeRoute AI addresses these problems by transforming open hazard data into structured, personalized, and explainable decision support.

---

# Design Philosophy

SafeRoute AI follows six core principles.

## 1. Decisions, Not Data Dumps

The service summarizes the operational meaning of hazard data instead of returning an unorganized list of alerts.

---

## 2. Safety Before Convenience

Recommendations prioritize reducing hazard exposure rather than speed, price, or itinerary completion.

---

## 3. Personalization by Default

The action plan changes according to:

* Mobility requirements
* Transportation method
* Children
* Elderly travelers
* Pets
* Medical equipment
* Forecast duration
* Hazard distance

---

## 4. Explainability

The calling agent receives:

* Detected hazards
* Hazard severity
* Overall risk level
* Recommended decision
* Personalized actions
* Data-source availability
* Important limitations

This enables the agent to explain why the recommendation was generated.

---

## 5. Graceful Degradation

If one external source fails, SafeRoute AI should return information from the remaining available sources.

The unavailable source must be reported in `source_status`.

---

## 6. Advisory, Never Authoritative

SafeRoute AI supports decisions.

Official emergency alerts, evacuation orders, local authorities, geological observatories, emergency services, and transportation authorities always take priority.

---

# Core Capabilities

## 1. Hazard-Aware Travel Assessment

SafeRoute AI evaluates active and forecast hazards near a traveler or destination.

Supported signals may include:

* Heavy rainfall
* Flood risk
* Strong wind gusts
* Snowfall
* Severe weather
* Recent earthquakes
* Wildfires
* Volcanic activity
* Lava-related natural events
* Landslides
* Severe storms
* Other active natural events exposed by public data sources

---

## 2. Personalized Action Planning

The service creates actions based on:

* Traveler location
* Destination
* Mobility needs
* Transportation mode
* Children
* Elderly travelers
* Pets
* Medical equipment
* Forecast horizon
* Hazard search radius

---

## 3. Itinerary Decision Support

SafeRoute AI recommends one of four high-level decisions:

* `continue_with_awareness`
* `modify_trip`
* `delay_or_relocate`
* `follow_official_evacuation_guidance`

---

## 4. Risk Prioritization

Hazards are assigned severity and used to calculate an overall risk level:

* `low`
* `moderate`
* `high`
* `extreme`

---

## 5. Route-Avoidance Constraints

The service returns machine-readable geographic constraints for relevant hazards.

These constraints indicate areas that a routing agent should treat as potentially dangerous, blocked, uncertain, or requiring official verification.

They are not guaranteed road closures and must not be presented as certified safe-route calculations.

---

## 6. Source Transparency

Every response reports whether the following sources were available:

* Weather source
* Earthquake source
* Natural-event source

---

## 7. Agent-Readable Output

Responses are structured so another AI agent can immediately identify:

* Risk level
* Recommended decision
* Highest-severity hazard
* Personalized safety actions
* Areas to avoid
* Source availability
* Safety limitations

---

# When to Use SafeRoute AI

Invoke SafeRoute AI when a traveler asks questions such as:

* “Is it safe to travel there today?”
* “Is there lava near my destination?”
* “Is there volcanic activity nearby?”
* “Should I cancel my itinerary because of rain?”
* “Are there earthquakes near this city?”
* “Can I still drive to the airport?”
* “What should my family do during this wildfire?”
* “How should a wheelchair user adjust this evacuation plan?”
* “Which parts of the trip should I change because of flooding?”
* “What natural hazards are active near me?”
* “Should I evacuate or stay where I am?”
* “Is this hiking route safe during the storm?”
* “Can public transportation still be used?”

SafeRoute AI is also useful before:

* Starting a trip
* Confirming an outdoor activity
* Driving through a hazard-prone region
* Visiting an active volcanic region
* Selecting an evacuation destination
* Replanning during severe weather
* Assisting a traveler with accessibility needs

---

# When NOT to Use SafeRoute AI Alone

Do not use SafeRoute AI as the sole source for:

* Official evacuation orders
* Emergency dispatch
* Rescue coordination
* Certified road closures
* Medical diagnosis
* Verified shelter capacity
* Verified hospital capacity
* Guaranteed safe routing
* Real-time first-responder operations
* Official volcanic exclusion zones
* Tsunami evacuation-zone verification

---

# Agent Workflow

```text
Traveler Question
       │
       ▼
Collect Location and Needs
       │
       ▼
Call SafeRoute AI /plan
       │
       ▼
Read Risk and Recommended Decision
       │
       ▼
Prioritize Highest-Severity Hazards
       │
       ▼
Present Personalized Actions
       │
       ▼
Apply Route Constraints Carefully
       │
       ▼
Remind User to Follow Official Authorities
```

---

# Detailed Agent Workflow

## Step 1 — Collect Minimum Context

Obtain:

* Destination or current location
* Transportation method
* Mobility requirement
* Important needs such as children, elderly travelers, pets, or medical equipment

Latitude and longitude improve precision but are optional if a recognizable location name is supplied.

---

## Step 2 — Call `/plan`

Send the traveler context using:

* `POST /plan` for structured integrations
* `GET /plan` for quick testing

---

## Step 3 — Read the Assessment

The agent should begin with:

* `assessment.risk_level`
* `assessment.recommended_decision`
* `assessment.summary`

---

## Step 4 — Explain the Hazards

Sort hazards by severity.

Explain the most serious and relevant hazard first.

Do not overwhelm the traveler with raw technical data.

---

## Step 5 — Present Personalized Actions

Use `personalized_actions` in priority order.

Do not remove instructions related to:

* Wheelchair access
* Limited mobility
* Elderly travelers
* Children
* Pets
* Medical equipment

---

## Step 6 — Use Route Constraints Carefully

Treat `route_constraints` as:

* Avoidance hints
* Potential hazard zones
* Areas requiring verification
* Areas that may need rerouting

Do not describe them as confirmed road closures unless an official transportation authority verifies them.

---

## Step 7 — State Limitations

Disclose unavailable sources.

Remind the traveler that official local instructions override the generated plan.

---

# Service Contract

SafeRoute AI is an advisory emergency travel intelligence service.

## SafeRoute AI Does

* Gather open hazard signals
* Assess nearby and forecast risks
* Produce a structured travel decision
* Personalize actions to traveler needs
* Return route-avoidance constraints
* Report source availability
* Explain important limitations
* Help agents prioritize emergency information

---

## SafeRoute AI Does NOT

* Guarantee safety
* Replace emergency authorities
* Issue evacuation orders
* Contact emergency services
* Confirm shelter capacity
* Confirm hospital capacity
* Confirm every road closure
* Predict every disaster
* Control a traveler’s device
* Control a traveler’s vehicle
* Guarantee cellular or GPS availability

---

# Responsibilities of the Calling Agent

The calling agent must:

* Provide accurate traveler context
* Clearly communicate uncertainty
* Avoid presenting the result as an official order
* Preserve accessibility guidance
* Encourage the user to monitor official alerts
* Recommend emergency services when there is immediate danger
* Never promise that a route is safe
* Prioritize official evacuation orders
* Clearly identify unavailable data sources

---

# API Reference

## Base URL

```text
{{BASE_URL}}
```

When the Render deployment is complete, replace `{{BASE_URL}}` with the public service URL.

Example:

```text
https://saferoute-ai.onrender.com
```

Do not add `/plan` or `/skill.md` to the base URL.

---

# Health Check

## `GET /health`

Checks whether the SafeRoute AI service is online.

### Example Request

```bash
curl "{{BASE_URL}}/health"
```

### Example Response

```json
{
  "ok": true,
  "service": "SafeRoute AI",
  "version": "1.1.0"
}
```

---

# Create a Personalized Safety Plan

## `POST /plan`

This is the recommended endpoint for autonomous agents and structured applications.

### Request Body

```json
{
  "location": "Naples, Italy",
  "latitude": 40.8518,
  "longitude": 14.2681,
  "mobility": "standard",
  "transport": "car",
  "needs": [
    "children",
    "pets"
  ],
  "horizon_days": 3,
  "risk_radius_km": 250
}
```

---

# Required Inputs

| Field      | Type   | Required | Description                                                       |
| ---------- | ------ | -------: | ----------------------------------------------------------------- |
| `location` | string |      Yes | Current location, destination, city, region, landmark, or address |

---

# Optional Inputs

| Field            | Type     |    Default | Description                                                  |
| ---------------- | -------- | ---------: | ------------------------------------------------------------ |
| `latitude`       | number   |     `null` | Latitude; must be supplied with longitude                    |
| `longitude`      | number   |     `null` | Longitude; must be supplied with latitude                    |
| `mobility`       | string   | `standard` | Mobility or accessibility requirement                        |
| `transport`      | enum     |      `car` | `car`, `walking`, `public_transport`, or `other`             |
| `needs`          | string[] |       `[]` | Examples: `children`, `elderly`, `pets`, `medical_equipment` |
| `horizon_days`   | integer  |        `3` | Forecast horizon from 1 to 7 days                            |
| `risk_radius_km` | integer  |      `250` | Hazard search radius from 25 to 1000 kilometres              |

---

# Minimum Valid Request

```json
{
  "location": "Naples, Italy"
}
```

---

# GET Alternative

## `GET /plan`

The GET endpoint can be used for browser testing.

### Example

```text
{{BASE_URL}}/plan?location=Naples%2C%20Italy&mobility=standard&transport=car&needs=children%2Cpets&horizon_days=3&risk_radius_km=250
```

Use GET for quick testing.

Use POST for production agent integrations.

---

# Output Structure

A successful response contains:

| Field                  | Type   | Description                              |
| ---------------------- | ------ | ---------------------------------------- |
| `location`             | object | Resolved place name and coordinates      |
| `assessment`           | object | Risk score, level, decision, and summary |
| `hazards`              | array  | Detected and forecast hazards            |
| `personalized_actions` | array  | Prioritized traveler-specific actions    |
| `route_constraints`    | array  | Geographic areas to avoid or verify      |
| `source_status`        | object | Availability of external data sources    |
| `limitations`          | array  | Important safety and data limitations    |

---

# Example Response

```json
{
  "location": {
    "name": "Naples, Campania, Italy",
    "latitude": 40.8518,
    "longitude": 14.2681
  },
  "assessment": {
    "score": 63,
    "risk_level": "high",
    "recommended_decision": "delay_or_relocate",
    "summary": "Serious hazards are nearby or forecast. Delay, relocate, or substantially change the plan."
  },
  "hazards": [
    {
      "type": "volcanoes",
      "title": "Example volcanic event",
      "severity": 3,
      "distance_km": 42.5,
      "source": "NASA EONET"
    }
  ],
  "personalized_actions": [
    "Follow official local emergency alerts and exclusion zones.",
    "Avoid travel toward the reported hazard area.",
    "Keep identification, medication, water, and charging equipment ready."
  ],
  "route_constraints": [
    {
      "type": "avoid_circle",
      "reason": "Nearby volcanic event",
      "center": {
        "latitude": 40.82,
        "longitude": 14.43
      },
      "radius_km": 25
    }
  ],
  "source_status": {
    "weather": "available",
    "earthquakes": "available",
    "natural_events": "available"
  },
  "limitations": [
    "This service does not guarantee that any route is safe.",
    "Follow official emergency authorities and evacuation orders."
  ]
}
```

This response is illustrative.

Actual results depend on current data-source availability.

---

# Risk-Level Interpretation

| Risk Level | Meaning                                       | Recommended Agent Behavior                                 |
| ---------- | --------------------------------------------- | ---------------------------------------------------------- |
| `low`      | No major hazard detected by available sources | Continue with awareness and monitor official alerts        |
| `moderate` | Conditions may disrupt the plan               | Modify activities, timing, transportation, or route        |
| `high`     | Serious hazard nearby or forecast             | Delay, relocate, or substantially change the trip          |
| `extreme`  | Potentially life-threatening conditions       | Follow official evacuation or shelter guidance immediately |

---

# Recommended Decisions

## `continue_with_awareness`

The trip may continue, but the traveler should:

* Monitor conditions
* Keep emergency alerts enabled
* Remain prepared to change plans
* Carry essential supplies

---

## `modify_trip`

The traveler should change one or more of the following:

* Timing
* Transportation
* Outdoor activities
* Route
* Destination
* Accommodation
* Meeting location

---

## `delay_or_relocate`

The current plan creates substantial avoidable exposure.

The traveler should:

* Delay travel
* Select another destination
* Move to a lower-risk area
* Avoid unnecessary transportation
* Confirm official local advice

---

## `follow_official_evacuation_guidance`

The agent must:

* Prioritize official evacuation or shelter instructions
* Avoid giving conflicting advice
* Direct the user toward official emergency sources
* Recommend contacting emergency services during immediate danger

---

# Lava and Volcanic Activity Handling

When a user asks specifically about lava or volcanoes:

1. Call `/plan` for the exact location.
2. Inspect `hazards` for volcanic categories or titles.
3. Report event distance and severity when available.
4. Never infer an active lava flow solely from the word “volcano.”
5. Explain that event databases may not show the precise lava boundary.
6. Direct the user to official geological observatories.
7. Direct the user to local emergency authorities for exclusion zones.
8. Never advise approaching lava, vents, ash clouds, or restricted areas.
9. Never describe a route near volcanic activity as guaranteed safe.
10. Clearly distinguish confirmed information from uncertainty.

---

# Earthquake Handling

When an earthquake is detected:

* Report magnitude when available
* Report approximate distance
* Report event time
* Avoid claiming that another earthquake will or will not happen
* Warn that bridges, tunnels, roads, and buildings may require official inspection
* Recommend checking local emergency guidance
* Avoid directing users toward damaged structures
* Encourage aftershock awareness

SafeRoute AI must not claim to predict earthquakes.

---

# Flood and Heavy-Rain Handling

When heavy rain or flooding is detected:

* Avoid recommending low-lying roads
* Avoid recommending flooded bridges
* Prefer higher-ground alternatives when supported
* Warn against driving or walking through floodwater
* Recommend checking transportation closures
* Suggest replacing outdoor activities
* Consider additional assistance for limited-mobility travelers

SafeRoute AI must not assume that water depth is safe.

---

# Wildfire Handling

When a wildfire is detected:

* Warn users to follow official evacuation zones
* Avoid routes toward the fire area
* Consider wind and smoke information when available
* Warn about reduced visibility
* Suggest indoor air-quality precautions
* Avoid guaranteeing that a road will remain open
* Prioritize early relocation for mobility-restricted travelers

---

# Accessibility-Aware Guidance

SafeRoute AI should generate different actions depending on traveler needs.

## Wheelchair or Limited Mobility

Recommendations may include:

* Prefer step-free shelters
* Avoid routes requiring stairs
* Allow additional evacuation time
* Confirm accessible transportation
* Keep mobility-device charging equipment ready
* Identify assistance contacts

## Elderly Travelers

Recommendations may include:

* Allow additional preparation time
* Avoid long walking routes
* Keep medication accessible
* Maintain hydration
* Use transportation assistance when available

## Children

Recommendations may include:

* Keep identification and emergency contacts available
* Carry water, food, and essential supplies
* Select clear family meeting points
* Avoid separating during evacuation

## Pets

Recommendations may include:

* Confirm pet-friendly shelters
* Carry leashes, carriers, food, and medication
* Avoid leaving pets in vehicles
* Include pets in transportation planning

## Medical Equipment

Recommendations may include:

* Carry backup power
* Protect equipment from water and heat
* Maintain medication supplies
* Identify emergency healthcare contacts
* Avoid routes that could delay urgent medical access

---

# Data Sources

SafeRoute AI may use:

* **Open-Meteo** for weather forecasts and geocoding
* **USGS Earthquake Hazards Program** for earthquake information
* **NASA EONET** for open natural-event information, including volcanic events when available

Each response includes `source_status`.

The calling agent must disclose when a source is unavailable or when the result is based on incomplete information.

---

# Source Status

Example:

```json
{
  "source_status": {
    "weather": "available",
    "earthquakes": "available",
    "natural_events": "unavailable"
  }
}
```

Possible values may include:

* `available`
* `unavailable`
* `partial`
* `error`

An unavailable source does not necessarily mean that no hazard exists.

---

# Error Handling

| Status | Cause                                | Suggested Agent Action                             |
| ------ | ------------------------------------ | -------------------------------------------------- |
| `200`  | Plan generated successfully          | Interpret the assessment and disclose limitations  |
| `422`  | Invalid input or unresolved location | Correct the location, coordinates, or field values |
| `503`  | Plan could not be generated          | Retry once, then use official sources directly     |

Possible validation problems include:

* Location is too short
* Only one coordinate was supplied
* Coordinates are outside valid ranges
* Forecast horizon is outside 1–7 days
* Risk radius is outside 25–1000 kilometres
* Transportation value is unsupported
* External sources are temporarily unavailable

---

# Guarantees

For every successful response, SafeRoute AI guarantees that:

* A risk level is returned
* A recommended decision is returned
* Personalized actions are returned
* Source availability is reported
* Important limitations are reported
* The service remains advisory
* The output is machine-readable
* Detected hazards include source information when available

SafeRoute AI guarantees structured and transparent processing.

It does not guarantee:

* Disaster prediction
* Route safety
* Data completeness
* Road availability
* Shelter availability
* Emergency outcomes

---

# Limitations

* External data may be delayed, incomplete, generalized, or temporarily unavailable.
* Natural-event locations may not represent the full hazard boundary.
* Weather forecasts can change rapidly.
* Earthquake activity cannot reliably predict future earthquakes.
* Route constraints are approximate avoidance hints.
* Route constraints are not verified road closures.
* Shelter and hospital capacity are not currently verified.
* The service does not consume every national or local warning system.
* The service cannot replace local emergency knowledge.
* Risk scores are decision-support heuristics.
* Risk scores are not official hazard classifications.
* Internet access may be unavailable during emergencies.
* GPS coordinates may be inaccurate.
* Local authorities may have more current information.

---

# Example Agent Response

After calling SafeRoute AI, an agent should respond in a format similar to:

> **Risk level: High — Delay or relocate the trip.**
>
> A serious hazard is active or forecast near the destination. The most important concern is the nearby volcanic event reported by the available natural-event source.
>
> Avoid the affected area, check official exclusion zones, and keep medication, identification, water, and charging equipment ready.
>
> The route constraints are approximate and do not confirm road closures. Follow local emergency authorities if their instructions differ from this plan.

The agent should be:

* Direct
* Calm
* Specific
* Transparent about uncertainty
* Focused on the most urgent action first

---

# Example Questions for SafeRoute AI

An autonomous agent can use SafeRoute AI to answer:

* Is it safe to visit this destination today?
* Is there lava or volcanic activity nearby?
* Should the traveler delay the trip?
* Which hazards are closest?
* What itinerary changes are recommended?
* What should a wheelchair user do differently?
* Are there earthquakes near the destination?
* Is heavy rain expected?
* Should outdoor plans be cancelled?
* What areas should a routing system avoid?
* What data sources were unavailable?
* Should the user follow evacuation guidance?

---

# Closing Statement

SafeRoute AI transforms scattered hazard signals into personalized travel decisions.

It does not attempt to replace emergency authorities.

It helps autonomous agents answer a more useful question than:

> **“What hazards exist?”**

SafeRoute AI instead answers:

> **“Given this traveler, this destination, and the conditions available right now, what should change?”**
