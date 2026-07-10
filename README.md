# SafeRoute Emergency Planner — NANDAHack Phase 2

SafeRoute is an agent-facing web service that combines:

- Open-Meteo forecasts
- USGS earthquake data
- NASA EONET active natural-event data
- Traveler mobility, transport, and special needs

It returns a risk score, itinerary decision, hazards, personalized actions, and machine-readable route constraints.

## Important NANDAHack distinction

Phase 2 is not an AI-agent implementation. You host this service and its `SKILL.md`. NANDA's judge agent reads the skill file and calls the service.

## Run locally

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open:

- Home: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Skill: http://127.0.0.1:8000/skill.md
- Health: http://127.0.0.1:8000/health

Example:

```bash
curl "http://127.0.0.1:8000/plan?location=Los%20Angeles&latitude=34.0522&longitude=-118.2437&mobility=wheelchair&transport=car&needs=elderly&horizon_days=3&risk_radius_km=300"
```

## Test

```bash
pytest -q
```

## Deploy to Render

1. Push this folder to a public GitHub repository.
2. In Render, choose **New → Blueprint** and select the repository. Render will detect `render.yaml`.
3. Deploy the web service.
4. After Render gives you a URL, add this environment variable:

```text
PUBLIC_BASE_URL=https://YOUR-SERVICE.onrender.com
```

5. Redeploy.
6. Test these public URLs:

```text
https://YOUR-SERVICE.onrender.com/health
https://YOUR-SERVICE.onrender.com/skill.md
https://YOUR-SERVICE.onrender.com/plan?location=Los%20Angeles&latitude=34.0522&longitude=-118.2437&mobility=wheelchair&transport=car&needs=elderly&horizon_days=3&risk_radius_km=300
```

The first free-tier request can be slow because the service may be waking up.

## NANDA Phase 2 submission values

- Skill name: `SafeRoute Emergency Planner`
- One-line description: `Turns a travel destination and accessibility needs into a live hazard assessment, itinerary decision, personalized actions, and route constraints.`
- Source type: Hosted link
- Skill link: `https://YOUR-SERVICE.onrender.com/skill.md`
- GitHub username: your bare username, not a URL
- Tags: `travel, disaster, emergency, weather, safety, accessibility, routing`
- Endpoints, one per line:

```text
GET https://YOUR-SERVICE.onrender.com/health
GET https://YOUR-SERVICE.onrender.com/plan?location=Los%20Angeles&latitude=34.0522&longitude=-118.2437&mobility=wheelchair&transport=car&needs=elderly&horizon_days=3&risk_radius_km=300
```

## Video demo outline

1. State the problem: normal maps optimize for speed, not hazard-aware decisions.
2. Open `/skill.md` and explain that this is all the judge agent receives.
3. Open the example `/plan` URL.
4. Point out `assessment`, `hazards`, `personalized_actions`, and `route_constraints`.
5. Change one traveler parameter, such as `mobility=wheelchair`, and show the personalized output.
6. End with: “SafeRoute does not replace official alerts; it turns trusted live data into agent-readable travel decisions.”

## Safety boundary

This project is a hackathon prototype. It must not be described as a guaranteed safe route, an evacuation order, or a replacement for emergency authorities.
