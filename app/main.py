import os
from pathlib import Path
import asyncio
import math
from datetime import datetime, timedelta, timezone

import httpx

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, PlainTextResponse


app = FastAPI(
    title="SafeRoute AI",
    version="1.1.0",
    description="Personalized disaster-aware travel decision support.",
)

BASE_URL = os.getenv(
    "RENDER_EXTERNAL_URL",
    "https://saferoute-travel-agent.onrender.com",
)

SKILL_FILE = Path(__file__).resolve().parent.parent / "SKILL.md"


HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta
        name="description"
        content="SafeRoute AI provides live disaster-aware travel guidance."
    >
    <title>SafeRoute AI</title>

    <style>
        :root {
            --bg: #07111f;
            --panel: #0d1e31;
            --panel-dark: #081524;
            --border: #243b55;
            --text: #f3f7fb;
            --muted: #a9c1da;
            --green: #61dfbd;
            --blue: #63adff;
            --yellow: #ffd66b;
            --orange: #ff9c62;
            --red: #ff6c7f;
        }

        * { box-sizing: border-box; }

        html { scroll-behavior: smooth; }

        body {
            margin: 0;
            min-height: 100vh;
            color: var(--text);
            background:
                radial-gradient(
                    circle at 12% 5%,
                    rgba(69, 143, 255, 0.15),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 85% 18%,
                    rgba(97, 223, 189, 0.10),
                    transparent 28%
                ),
                var(--bg);
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        a { color: inherit; }

        .container {
            width: min(1480px, calc(100% - 30px));
            margin: 0 auto;
        }

        nav {
            position: sticky;
            top: 0;
            z-index: 20;
            border-bottom: 1px solid var(--border);
            background: rgba(7, 17, 31, 0.88);
            backdrop-filter: blur(16px);
        }

        .nav-inner {
            min-height: 68px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 850;
            text-decoration: none;
        }

        .logo {
            width: 38px;
            height: 38px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(97, 223, 189, 0.32);
            border-radius: 12px;
            background: rgba(97, 223, 189, 0.08);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .nav-links a {
            color: var(--muted);
            font-size: 14px;
            text-decoration: none;
        }

        .nav-links a:hover { color: var(--text); }

        .hero {
            padding: 78px 0 44px;
            text-align: center;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 13px;
            border: 1px solid rgba(97, 223, 189, 0.27);
            border-radius: 999px;
            color: var(--green);
            background: rgba(97, 223, 189, 0.07);
            font-size: 13px;
            font-weight: 800;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 14px var(--green);
        }

        h1 {
            max-width: 900px;
            margin: 24px auto 18px;
            font-size: clamp(44px, 7vw, 78px);
            line-height: 1;
            letter-spacing: -0.06em;
        }

        .gradient-text {
            background: linear-gradient(105deg, #ffffff, #7cb8ff, #61dfbd);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero p {
            max-width: 760px;
            margin: 0 auto;
            color: var(--muted);
            font-size: clamp(16px, 2vw, 20px);
            line-height: 1.65;
        }

        .hero-actions {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 28px;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 46px;
            padding: 0 18px;
            border: 1px solid var(--border);
            border-radius: 11px;
            font-weight: 800;
            text-decoration: none;
        }

        .button-primary {
            color: #06141d;
            border-color: transparent;
            background: linear-gradient(135deg, var(--green), var(--blue));
        }

        .button-secondary {
            background: rgba(255,255,255,0.04);
        }

        section { padding: 54px 0; }

        .section-heading {
            max-width: 760px;
            margin-bottom: 28px;
        }

        .eyebrow {
            margin: 0 0 8px;
            color: var(--green);
            font-size: 12px;
            font-weight: 850;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        h2 {
            margin: 0;
            font-size: clamp(30px, 4vw, 48px);
            letter-spacing: -0.045em;
        }

        .section-heading p {
            margin: 12px 0 0;
            color: var(--muted);
            line-height: 1.65;
        }

        .planner-grid {
            display: grid;
            grid-template-columns: 0.82fr 1fr 1.08fr;
            gap: 16px;
            align-items: stretch;
        }

        .panel {
            min-height: 620px;
            padding: 24px;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: rgba(13, 30, 49, 0.95);
            box-shadow: 0 24px 80px rgba(0,0,0,0.18);
        }

        .panel-title {
            margin: 0 0 6px;
            font-size: 22px;
        }

        .panel-description {
            margin: 0 0 22px;
            color: var(--muted);
            line-height: 1.55;
            font-size: 14px;
        }

        .form-row { margin-bottom: 16px; }

        label {
            display: block;
            margin-bottom: 7px;
            font-size: 13px;
            font-weight: 800;
        }

        input,
        select {
            width: 100%;
            min-height: 46px;
            padding: 0 13px;
            border: 1px solid var(--border);
            border-radius: 11px;
            outline: none;
            color: var(--text);
            background: var(--panel-dark);
            font: inherit;
        }

        input:focus,
        select:focus { border-color: var(--blue); }

        select option { color: #111827; }

        button {
            width: 100%;
            min-height: 48px;
            border: 0;
            border-radius: 12px;
            color: #07111f;
            background: linear-gradient(135deg, var(--green), var(--blue));
            font: inherit;
            font-weight: 900;
            cursor: pointer;
        }

        button:disabled {
            opacity: 0.65;
            cursor: wait;
        }

        .notice {
            margin-top: 16px;
            padding: 13px;
            border: 1px solid rgba(255, 214, 107, 0.23);
            border-radius: 11px;
            color: #f6dd99;
            background: rgba(255, 214, 107, 0.06);
            font-size: 12px;
            line-height: 1.5;
        }

        .empty-state {
            min-height: 465px;
            display: grid;
            place-items: center;
            padding: 28px;
            border: 1px dashed var(--border);
            border-radius: 14px;
            color: var(--muted);
            text-align: center;
        }

        .hidden { display: none; }

        .live-badge,
        .risk-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 11px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(255,255,255,0.04);
            font-size: 12px;
            font-weight: 850;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 13px var(--green);
        }

        .location-name {
            margin: 16px 0 4px;
            font-size: 20px;
        }

        .generated-time {
            margin: 0;
            color: var(--muted);
            font-size: 12px;
        }

        .weather-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 9px;
            margin-top: 17px;
        }

        .weather-card {
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 11px;
            background: var(--panel-dark);
        }

        .weather-value {
            display: block;
            margin-bottom: 3px;
            font-size: 18px;
            font-weight: 900;
        }

        .weather-label {
            color: var(--muted);
            font-size: 11px;
        }

        .hazard-list {
            display: grid;
            gap: 10px;
            margin-top: 16px;
        }

        .hazard-card {
            padding: 14px;
            border: 1px solid var(--border);
            border-radius: 13px;
            background: var(--panel-dark);
        }

        .hazard-top {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 7px;
        }

        .hazard-title {
            font-weight: 850;
            line-height: 1.35;
        }

        .hazard-distance {
            flex-shrink: 0;
            color: var(--muted);
            font-size: 11px;
        }

        .hazard-category {
            display: inline-block;
            margin-bottom: 7px;
            padding: 4px 7px;
            border-radius: 6px;
            color: var(--blue);
            background: rgba(99, 173, 255, 0.09);
            font-size: 10px;
            font-weight: 850;
            text-transform: uppercase;
        }

        .hazard-details {
            margin: 0;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .hazard-source {
            display: block;
            margin-top: 8px;
            color: #7894ae;
            font-size: 10px;
        }

        .no-hazard {
            margin-top: 16px;
            padding: 17px;
            border: 1px solid rgba(97, 223, 189, 0.32);
            border-radius: 13px;
            background: rgba(97, 223, 189, 0.07);
        }

        .no-hazard strong { color: var(--green); }

        .no-hazard p {
            margin: 7px 0 0;
            color: var(--muted);
            line-height: 1.5;
            font-size: 13px;
        }

        .source-list {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 16px;
        }

        .source-pill {
            padding: 5px 8px;
            border: 1px solid var(--border);
            border-radius: 999px;
            color: var(--muted);
            font-size: 10px;
        }

        .decision {
            margin: 17px 0 10px;
            font-size: 24px;
            text-transform: capitalize;
        }

        .summary {
            color: var(--muted);
            line-height: 1.6;
        }

        .actions {
            padding-left: 20px;
            color: var(--muted);
        }

        .actions li {
            margin-bottom: 9px;
            line-height: 1.5;
        }

        .risk-low { color: var(--green); }
        .risk-moderate { color: var(--yellow); }
        .risk-high { color: var(--orange); }
        .risk-extreme { color: var(--red); }

        footer {
            margin-top: 22px;
            padding: 34px 0 45px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 13px;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 14px;
        }

        @media (max-width: 1120px) {
            .planner-grid {
                grid-template-columns: 1fr 1fr;
            }

            .form-panel {
                grid-column: 1 / -1;
                min-height: auto;
            }
        }

        @media (max-width: 760px) {
            .planner-grid { grid-template-columns: 1fr; }
            .form-panel { grid-column: auto; }
            .panel { min-height: auto; }

            .nav-links a:not(.button) { display: none; }
        }

        @media (max-width: 500px) {
            .weather-grid { grid-template-columns: 1fr; }
            .container { width: min(100% - 20px, 1480px); }
        }
    </style>
</head>

<body>
    <nav>
        <div class="container nav-inner">
            <a class="brand" href="/">
                <span class="logo">🧭</span>
                <span>SafeRoute AI</span>
            </a>

            <div class="nav-links">
                <a href="#planner">Live planner</a>
                <a href="/docs">API</a>
                <a class="button button-secondary" href="/skill-preview">
                    SkillMD
                </a>
            </div>
        </div>
    </nav>

    <main>
        <section class="hero">
            <div class="container">
                <div class="badge">
                    <span class="status-dot"></span>
                    Live disaster-aware travel intelligence
                </div>

                <h1>
                    Know what is happening.
                    <span class="gradient-text">Know what to do next.</span>
                </h1>

                <p>
                    SafeRoute checks live weather, earthquakes and natural
                    events, then creates a plan personalized to the traveler’s
                    transport, mobility, family, pet and medical needs.
                </p>

                <div class="hero-actions">
                    <a class="button button-primary" href="#planner">
                        Generate a live plan
                    </a>

                    <a class="button button-secondary" href="/skill-preview">
                        View SkillMD
                    </a>
                </div>
            </div>
        </section>

        <section id="planner">
            <div class="container">
                <div class="section-heading">
                    <p class="eyebrow">Live planner</p>
                    <h2>Generate a personalized safety plan.</h2>
                    <p>
                        The middle panel shows what the connected feeds detect.
                        The right panel converts that information into actions
                        for the specific traveler.
                    </p>
                </div>

                <div class="planner-grid">
                    <section class="panel form-panel">
                        <h3 class="panel-title">Traveler details</h3>

                        <p class="panel-description">
                            Enter the destination and exact traveler needs.
                        </p>

                        <form id="planner-form">
                            <div class="form-row">
                                <label for="location">
                                    Location or destination
                                </label>

                                <input
                                    id="location"
                                    name="location"
                                    value="Naples, Italy"
                                    minlength="2"
                                    required
                                >
                            </div>

                            <div class="form-row">
                                <label for="mobility">
                                    Mobility requirement
                                </label>

                                <select id="mobility" name="mobility">
                                    <option value="standard">Standard</option>
                                    <option value="wheelchair">Wheelchair</option>
                                    <option value="limited mobility">
                                        Limited mobility
                                    </option>
                                </select>
                            </div>

                            <div class="form-row">
                                <label for="transport">Transportation</label>

                                <select id="transport" name="transport">
                                    <option value="car">Car</option>
                                    <option value="walking">Walking</option>
                                    <option value="public_transport">
                                        Public transport
                                    </option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div class="form-row">
                                <label for="needs">Additional needs</label>

                                <input
                                    id="needs"
                                    name="needs"
                                    value="children,pets"
                                    placeholder="dog,children,medical,elderly"
                                >
                            </div>

                            <div class="form-row">
                                <label for="risk-radius">
                                    Hazard search radius
                                </label>

                                <select
                                    id="risk-radius"
                                    name="risk_radius_km"
                                >
                                    <option value="100">100 km</option>
                                    <option value="300" selected>300 km</option>
                                    <option value="500">500 km</option>
                                    <option value="1000">1000 km</option>
                                </select>
                            </div>

                            <button id="submit-button" type="submit">
                                Check live feeds
                            </button>
                        </form>

                        <div class="notice">
                            Uses Open-Meteo, USGS and NASA EONET. Official
                            emergency instructions always take priority.
                        </div>
                    </section>

                    <section class="panel">
                        <h3 class="panel-title">What is happening?</h3>

                        <p class="panel-description">
                            Live weather, earthquakes and natural events near
                            the selected location.
                        </p>

                        <div id="hazard-empty" class="empty-state">
                            Generate a plan to check the live hazard feeds.
                        </div>

                        <div id="hazard-content" class="hidden">
                            <span class="live-badge">
                                <span class="live-dot"></span>
                                Live feed result
                            </span>

                            <h3
                                id="resolved-location"
                                class="location-name"
                            ></h3>

                            <p
                                id="generated-time"
                                class="generated-time"
                            ></p>

                            <div
                                id="weather-grid"
                                class="weather-grid"
                            ></div>

                            <div
                                id="hazard-list"
                                class="hazard-list"
                            ></div>

                            <div
                                id="source-list"
                                class="source-list"
                            ></div>
                        </div>
                    </section>

                    <section class="panel">
                        <h3 class="panel-title">Your personalized plan</h3>

                        <p class="panel-description">
                            Recommendations based on the live result and the
                            traveler’s individual needs.
                        </p>

                        <div id="plan-empty" class="empty-state">
                            Your customized actions will appear here.
                        </div>

                        <div id="plan-content" class="hidden">
                            <span
                                id="risk-badge"
                                class="risk-badge"
                            ></span>

                            <h3 id="decision" class="decision"></h3>

                            <p id="summary" class="summary"></p>

                            <h3>Personalized actions</h3>

                            <ul id="actions" class="actions"></ul>
                        </div>
                    </section>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container footer-inner">
            <span>SafeRoute AI · NANDA Town Hackathon</span>
            <span>
                Decision support only — never a replacement for authorities
            </span>
        </div>
    </footer>

    <script>
        const form = document.getElementById("planner-form");
        const submitButton = document.getElementById("submit-button");

        const hazardEmpty = document.getElementById("hazard-empty");
        const hazardContent = document.getElementById("hazard-content");
        const resolvedLocation = document.getElementById("resolved-location");
        const generatedTime = document.getElementById("generated-time");
        const weatherGrid = document.getElementById("weather-grid");
        const hazardList = document.getElementById("hazard-list");
        const sourceList = document.getElementById("source-list");

        const planEmpty = document.getElementById("plan-empty");
        const planContent = document.getElementById("plan-content");
        const riskBadge = document.getElementById("risk-badge");
        const decision = document.getElementById("decision");
        const summary = document.getElementById("summary");
        const actions = document.getElementById("actions");


        function createElement(tag, className, text) {
            const element = document.createElement(tag);

            if (className) {
                element.className = className;
            }

            if (text !== undefined && text !== null) {
                element.textContent = String(text);
            }

            return element;
        }


        function hazardIcon(category) {
            const text = String(category || "").toLowerCase();

            if (text.includes("earthquake")) return "🌎";
            if (text.includes("volcano")) return "🌋";
            if (text.includes("wildfire")) return "🔥";
            if (text.includes("flood")) return "🌊";
            if (text.includes("rain")) return "🌧️";
            if (text.includes("storm")) return "⛈️";
            if (text.includes("wind")) return "💨";
            if (text.includes("snow")) return "❄️";
            if (text.includes("landslide")) return "🪨";

            return "⚠️";
        }


        function formatNumber(value, suffix) {
            const number = Number(value);

            if (!Number.isFinite(number)) {
                return "—";
            }

            return `${number.toFixed(1)}${suffix}`;
        }


        function renderWeather(weather) {
            weatherGrid.replaceChildren();

            const weatherItems = [
                [
                    "Temperature",
                    formatNumber(weather.temperature_c, "°C")
                ],
                [
                    "Current wind",
                    formatNumber(weather.current_wind_kmh, " km/h")
                ],
                [
                    "3-day precipitation",
                    formatNumber(
                        weather.maximum_3_day_precipitation_mm,
                        " mm"
                    )
                ],
                [
                    "Maximum gust",
                    formatNumber(
                        weather.maximum_3_day_gust_kmh,
                        " km/h"
                    )
                ]
            ];

            for (const [label, value] of weatherItems) {
                const card = createElement("div", "weather-card");
                card.appendChild(
                    createElement("span", "weather-value", value)
                );
                card.appendChild(
                    createElement("span", "weather-label", label)
                );
                weatherGrid.appendChild(card);
            }
        }


        function renderHazards(hazards) {
            hazardList.replaceChildren();

            if (!hazards.length) {
                const box = createElement("div", "no-hazard");
                box.appendChild(
                    createElement(
                        "strong",
                        "",
                        "No major active disaster detected."
                    )
                );
                box.appendChild(
                    createElement(
                        "p",
                        "",
                        "The connected feeds did not find a major nearby " +
                        "event. This does not guarantee that conditions " +
                        "are safe."
                    )
                );
                hazardList.appendChild(box);
                return;
            }

            for (const hazard of hazards.slice(0, 6)) {
                const card = createElement("article", "hazard-card");

                card.appendChild(
                    createElement(
                        "span",
                        "hazard-category",
                        hazard.category || hazard.type || "Hazard"
                    )
                );

                const top = createElement("div", "hazard-top");

                top.appendChild(
                    createElement(
                        "div",
                        "hazard-title",
                        `${hazardIcon(hazard.category)} ${hazard.title}`
                    )
                );

                const distance = Number(hazard.distance_km);

                top.appendChild(
                    createElement(
                        "div",
                        "hazard-distance",
                        Number.isFinite(distance)
                            ? `${distance.toFixed(1)} km away`
                            : "Nearby"
                    )
                );

                card.appendChild(top);

                card.appendChild(
                    createElement(
                        "p",
                        "hazard-details",
                        hazard.details || ""
                    )
                );

                card.appendChild(
                    createElement(
                        "span",
                        "hazard-source",
                        `Source: ${hazard.source || "Unknown"}`
                    )
                );

                hazardList.appendChild(card);
            }
        }


        function renderSources(sourceStatus) {
            sourceList.replaceChildren();

            for (const [source, status] of Object.entries(sourceStatus || {})) {
                sourceList.appendChild(
                    createElement(
                        "span",
                        "source-pill",
                        `${source}: ${status}`
                    )
                );
            }
        }


        function renderPlan(data) {
            const level = data.assessment?.risk_level || "unknown";

            riskBadge.className = `risk-badge risk-${level}`;
            riskBadge.textContent = `Risk level: ${level.toUpperCase()}`;

            decision.textContent = (
                data.assessment?.recommended_decision
                || "continue_with_awareness"
            ).replaceAll("_", " ");

            summary.textContent = data.assessment?.summary || "";

            actions.replaceChildren();

            for (const action of data.personalized_actions || []) {
                actions.appendChild(createElement("li", "", action));
            }
        }


        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            submitButton.disabled = true;
            submitButton.textContent = "Checking live feeds...";

            hazardEmpty.classList.remove("hidden");
            hazardEmpty.textContent =
                "Checking Open-Meteo, USGS and NASA EONET...";
            hazardContent.classList.add("hidden");

            planEmpty.classList.remove("hidden");
            planEmpty.textContent =
                "Building the personalized action plan...";
            planContent.classList.add("hidden");

            const formData = new FormData(form);
            const params = new URLSearchParams(formData);

            try {
                const response = await fetch(`/plan?${params.toString()}`);
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(
                        data.detail || "The plan could not be generated."
                    );
                }

                resolvedLocation.textContent =
                    data.location?.name || formData.get("location");

                generatedTime.textContent = data.generated_at
                    ? `Updated ${new Date(
                        data.generated_at
                    ).toLocaleString()}`
                    : "";

                renderWeather(data.weather || {});
                renderHazards(data.hazards || []);
                renderSources(data.source_status || {});
                renderPlan(data);

                hazardEmpty.classList.add("hidden");
                hazardContent.classList.remove("hidden");

                planEmpty.classList.add("hidden");
                planContent.classList.remove("hidden");
            } catch (error) {
                hazardEmpty.classList.remove("hidden");
                hazardEmpty.textContent = error.message;
                hazardContent.classList.add("hidden");

                planEmpty.classList.remove("hidden");
                planEmpty.textContent =
                    "No personalized plan was generated.";
                planContent.classList.add("hidden");
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Check live feeds";
            }
        });
    </script>
</body>
</html>
"""



SKILL_PREVIEW_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>SafeRoute AI · SkillMD</title>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <style>
        :root {
            --background: #07111f;
            --surface: #0e1d2d;
            --border: rgba(148, 180, 209, 0.2);
            --text: #eef6fc;
            --muted: #a8bbcc;
            --green: #5ee6b8;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            color: var(--text);
            background:
                radial-gradient(
                    circle at 15% 8%,
                    rgba(65, 155, 255, 0.16),
                    transparent 30%
                ),
                var(--background);
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                sans-serif;
        }

        .topbar {
            position: sticky;
            top: 0;
            z-index: 10;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border);
            background: rgba(7, 17, 31, 0.88);
            backdrop-filter: blur(16px);
        }

        .topbar-inner {
            width: min(980px, 100%);
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
        }

        .topbar a {
            color: var(--text);
            text-decoration: none;
            font-weight: 750;
        }

        .raw-link {
            padding: 9px 13px;
            border: 1px solid var(--border);
            border-radius: 9px;
            font-size: 13px;
        }

        article {
            width: min(900px, calc(100% - 28px));
            margin: 36px auto 70px;
            padding: clamp(24px, 6vw, 58px);
            border: 1px solid var(--border);
            border-radius: 18px;
            background: rgba(14, 29, 45, 0.9);
            box-shadow: 0 30px 100px rgba(0, 0, 0, 0.24);
        }

        h1,
        h2,
        h3 {
            line-height: 1.2;
        }

        h1 {
            margin-top: 0;
            font-size: clamp(42px, 8vw, 66px);
            letter-spacing: -0.055em;
        }

        h2 {
            margin-top: 48px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            font-size: 29px;
        }

        h3 {
            margin-top: 30px;
        }

        p,
        li {
            color: #c2d2df;
            line-height: 1.75;
        }

        a {
            color: #78baff;
        }

        blockquote {
            margin: 24px 0;
            padding: 12px 18px;
            border-left: 4px solid var(--green);
            color: #d9f8ee;
            background: rgba(94, 230, 184, 0.06);
        }

        blockquote p {
            margin: 0;
            color: inherit;
        }

        table {
            width: 100%;
            display: block;
            overflow-x: auto;
            border-collapse: collapse;
            margin: 22px 0;
        }

        th,
        td {
            padding: 12px 14px;
            border: 1px solid var(--border);
            text-align: left;
        }

        th {
            background: rgba(255, 255, 255, 0.055);
        }

        code {
            padding: 2px 6px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.07);
        }

        pre {
            overflow-x: auto;
            padding: 18px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: #06101c;
        }

        pre code {
            padding: 0;
            background: transparent;
        }

        hr {
            margin: 34px 0;
            border: 0;
            border-top: 1px solid var(--border);
        }

        .loading {
            color: var(--muted);
        }
    </style>
</head>

<body>
    <header class="topbar">
        <div class="topbar-inner">
            <a href="/">← SafeRoute AI</a>

            <a class="raw-link" href="/skill.md">
                View raw Markdown
            </a>
        </div>
    </header>

    <article id="content">
        <p class="loading">Loading SkillMD preview...</p>
    </article>

    <script>
        async function loadSkill() {
            const content = document.getElementById("content");

            try {
                const response = await fetch("/skill.md");

                if (!response.ok) {
                    throw new Error("Could not load SKILL.md.");
                }

                const markdownText = await response.text();
                content.innerHTML = marked.parse(markdownText);
            } catch (error) {
                content.innerHTML = `<h1>Error</h1><p>${error.message}</p>`;
            }
        }

        loadSkill();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def homepage() -> str:
    return HOME_PAGE


@app.get("/health")
def health() -> dict:
    return {
        "ok": True,
        "service": "SafeRoute AI",
        "version": "1.1.0",
        "website": BASE_URL,
    }


# -------------------------------------------------------------------
# LIVE DISASTER DATA
# -------------------------------------------------------------------

OPEN_METEO_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"
USGS_EARTHQUAKES = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NASA_EONET = "https://eonet.gsfc.nasa.gov/api/v3/events"


def safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def max_number(values) -> float:
    valid = [
        safe_float(value)
        for value in (values or [])
        if value is not None
    ]
    return max(valid) if valid else 0.0


def haversine_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    earth_radius_km = 6371.0

    lat_1 = math.radians(latitude_1)
    lat_2 = math.radians(latitude_2)
    delta_lat = math.radians(latitude_2 - latitude_1)
    delta_lon = math.radians(longitude_2 - longitude_1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat_1)
        * math.cos(lat_2)
        * math.sin(delta_lon / 2) ** 2
    )

    return earth_radius_km * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )


def extract_coordinate_pairs(value) -> list[tuple[float, float]]:
    """
    Converts Point, Polygon or MultiPolygon coordinates into lon/lat pairs.
    """

    pairs: list[tuple[float, float]] = []

    if not isinstance(value, list):
        return pairs

    if (
        len(value) >= 2
        and isinstance(value[0], (int, float))
        and isinstance(value[1], (int, float))
    ):
        pairs.append((float(value[0]), float(value[1])))
        return pairs

    for item in value:
        pairs.extend(extract_coordinate_pairs(item))

    return pairs


def representative_coordinate(
    geometry: dict,
) -> tuple[float, float] | None:
    pairs = extract_coordinate_pairs(geometry.get("coordinates"))

    if not pairs:
        return None

    longitude = sum(pair[0] for pair in pairs) / len(pairs)
    latitude = sum(pair[1] for pair in pairs) / len(pairs)

    return latitude, longitude


async def resolve_location(
    client: httpx.AsyncClient,
    location: str,
) -> dict:
    response = await client.get(
        OPEN_METEO_GEOCODING,
        params={
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )
    response.raise_for_status()

    results = response.json().get("results") or []

    if not results:
        raise ValueError(
            "Location could not be found. Try adding the country or region."
        )

    place = results[0]

    display_parts = [
        place.get("name"),
        place.get("admin1"),
        place.get("country"),
    ]

    return {
        "name": ", ".join(
            part for part in display_parts if part
        ),
        "latitude": safe_float(place.get("latitude")),
        "longitude": safe_float(place.get("longitude")),
        "timezone": place.get("timezone"),
    }


async def fetch_weather(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
) -> tuple[dict, list[dict]]:
    response = await client.get(
        OPEN_METEO_FORECAST,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "precipitation,"
                "rain,"
                "weather_code,"
                "wind_speed_10m,"
                "wind_gusts_10m"
            ),
            "daily": (
                "weather_code,"
                "precipitation_sum,"
                "rain_sum,"
                "snowfall_sum,"
                "wind_gusts_10m_max"
            ),
            "timezone": "auto",
            "forecast_days": 3,
        },
    )
    response.raise_for_status()

    data = response.json()
    current = data.get("current") or {}
    daily = data.get("daily") or {}

    precipitation_max = max_number(
        daily.get("precipitation_sum")
    )
    rain_max = max_number(daily.get("rain_sum"))
    snow_max = max_number(daily.get("snowfall_sum"))
    gust_max = max_number(daily.get("wind_gusts_10m_max"))
    weather_codes = daily.get("weather_code") or []

    hazards: list[dict] = []

    if precipitation_max >= 50 or rain_max >= 50:
        hazards.append({
            "type": "weather",
            "category": "Heavy Rain",
            "title": "Very heavy rainfall forecast",
            "severity": 4,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                f"Up to {precipitation_max:.1f} mm of precipitation "
                "is forecast during the next three days."
            ),
        })
    elif precipitation_max >= 25 or rain_max >= 25:
        hazards.append({
            "type": "weather",
            "category": "Heavy Rain",
            "title": "Heavy rainfall forecast",
            "severity": 3,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                f"Up to {precipitation_max:.1f} mm of precipitation "
                "is forecast during the next three days."
            ),
        })
    elif precipitation_max >= 10 or rain_max >= 10:
        hazards.append({
            "type": "weather",
            "category": "Rain",
            "title": "Rain may disrupt travel",
            "severity": 2,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                f"Up to {precipitation_max:.1f} mm of precipitation "
                "is forecast."
            ),
        })

    if gust_max >= 90:
        severity = 4
    elif gust_max >= 65:
        severity = 3
    elif gust_max >= 45:
        severity = 2
    else:
        severity = 0

    if severity:
        hazards.append({
            "type": "weather",
            "category": "Strong Wind",
            "title": "Strong wind gusts forecast",
            "severity": severity,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                f"Maximum forecast gusts are approximately "
                f"{gust_max:.1f} km/h."
            ),
        })

    if snow_max >= 15:
        snow_severity = 3
    elif snow_max >= 5:
        snow_severity = 2
    else:
        snow_severity = 0

    if snow_severity:
        hazards.append({
            "type": "weather",
            "category": "Snow",
            "title": "Snow may disrupt transportation",
            "severity": snow_severity,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                f"Up to {snow_max:.1f} cm of snowfall is forecast."
            ),
        })

    if any(
        safe_float(code) in {95, 96, 99}
        for code in weather_codes
    ):
        hazards.append({
            "type": "weather",
            "category": "Thunderstorm",
            "title": "Thunderstorm conditions forecast",
            "severity": 3,
            "distance_km": 0,
            "source": "Open-Meteo",
            "details": (
                "Thunderstorms are included in the three-day forecast."
            ),
        })

    snapshot = {
        "temperature_c": safe_float(
            current.get("temperature_2m")
        ),
        "current_precipitation_mm": safe_float(
            current.get("precipitation")
        ),
        "current_wind_kmh": safe_float(
            current.get("wind_speed_10m")
        ),
        "current_gust_kmh": safe_float(
            current.get("wind_gusts_10m")
        ),
        "maximum_3_day_precipitation_mm": precipitation_max,
        "maximum_3_day_gust_kmh": gust_max,
        "maximum_3_day_snowfall_cm": snow_max,
    }

    return snapshot, hazards


async def fetch_earthquakes(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
    radius_km: int,
) -> list[dict]:
    start_time = (
        datetime.now(timezone.utc) - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    response = await client.get(
        USGS_EARTHQUAKES,
        params={
            "format": "geojson",
            "starttime": start_time,
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": radius_km,
            "minmagnitude": 2.5,
            "orderby": "time",
            "limit": 20,
        },
    )
    response.raise_for_status()

    hazards: list[dict] = []

    for feature in response.json().get("features") or []:
        properties = feature.get("properties") or {}
        coordinates = (
            feature.get("geometry", {}).get("coordinates") or []
        )

        if len(coordinates) < 2:
            continue

        event_longitude = safe_float(coordinates[0])
        event_latitude = safe_float(coordinates[1])
        magnitude = safe_float(properties.get("mag"))

        distance = haversine_km(
            latitude,
            longitude,
            event_latitude,
            event_longitude,
        )

        if magnitude >= 7:
            severity = 4
        elif magnitude >= 6 or (
            magnitude >= 5 and distance <= 100
        ):
            severity = 3
        elif magnitude >= 4 or distance <= 50:
            severity = 2
        else:
            severity = 1

        event_timestamp = properties.get("time")

        event_time = None
        if event_timestamp:
            event_time = datetime.fromtimestamp(
                event_timestamp / 1000,
                tz=timezone.utc,
            ).isoformat()

        hazards.append({
            "type": "earthquake",
            "category": "Earthquake",
            "title": f"Magnitude {magnitude:.1f} earthquake",
            "severity": severity,
            "distance_km": round(distance, 1),
            "source": "USGS",
            "details": properties.get("place")
            or "Recent earthquake",
            "event_time": event_time,
            "latitude": event_latitude,
            "longitude": event_longitude,
            "source_url": properties.get("url"),
        })

    return hazards[:8]


async def fetch_natural_events(
    client: httpx.AsyncClient,
    latitude: float,
    longitude: float,
    radius_km: int,
) -> list[dict]:
    response = await client.get(
        NASA_EONET,
        params={
            "status": "open",
            "days": 30,
            "limit": 200,
        },
    )
    response.raise_for_status()

    severity_by_category = {
        "volcanoes": 3,
        "wildfires": 3,
        "floods": 3,
        "landslides": 3,
        "severestorms": 3,
        "drought": 2,
        "dusthaze": 2,
        "snow": 2,
        "tempExtremes": 2,
    }

    hazards: list[dict] = []

    for event in response.json().get("events") or []:
        geometries = event.get("geometry") or []

        if not geometries:
            continue

        latest_geometry = geometries[-1]
        coordinate = representative_coordinate(latest_geometry)

        if coordinate is None:
            continue

        event_latitude, event_longitude = coordinate

        distance = haversine_km(
            latitude,
            longitude,
            event_latitude,
            event_longitude,
        )

        if distance > radius_km:
            continue

        categories = event.get("categories") or []

        category_title = (
            categories[0].get("title")
            if categories
            else "Natural Event"
        )

        category_id = (
            categories[0].get("id")
            if categories
            else "naturalEvent"
        )

        severity = severity_by_category.get(
            category_id,
            severity_by_category.get(
                str(category_id).lower(),
                2,
            ),
        )

        if distance <= 50:
            severity = min(4, severity + 1)

        source_links = [
            source.get("url")
            for source in event.get("sources") or []
            if source.get("url")
        ]

        hazards.append({
            "type": "natural_event",
            "category": category_title,
            "title": event.get("title") or category_title,
            "severity": severity,
            "distance_km": round(distance, 1),
            "source": "NASA EONET",
            "details": (
                f"Open {category_title.lower()} event approximately "
                f"{distance:.1f} km from the selected location."
            ),
            "event_time": latest_geometry.get("date"),
            "latitude": event_latitude,
            "longitude": event_longitude,
            "source_url": (
                source_links[0] if source_links else None
            ),
        })

    hazards.sort(
        key=lambda hazard: (
            -hazard["severity"],
            hazard["distance_km"],
        )
    )

    return hazards[:10]


def build_personalized_actions(
    hazards: list[dict],
    risk_level: str,
    mobility: str,
    transport: str,
    needs: str,
) -> list[str]:
    actions: list[str] = []

    # Show the most important live information first.
    for hazard in hazards[:3]:
        actions.append(
            f"Live signal: {hazard['title']} — "
            f"{hazard['details']}"
        )

    if risk_level == "extreme":
        actions.append(
            "Follow official evacuation or shelter instructions immediately."
        )
    elif risk_level == "high":
        actions.append(
            "Delay, relocate, or substantially change the travel plan."
        )
    elif risk_level == "moderate":
        actions.append(
            "Modify the route, timing, transportation, or outdoor activities."
        )
    else:
        actions.append(
            "Continue with awareness and keep official alerts enabled."
        )

    categories = {
        str(hazard.get("category", "")).lower()
        for hazard in hazards
    }

    hazard_types = {
        str(hazard.get("type", "")).lower()
        for hazard in hazards
    }

    if "earthquake" in hazard_types:
        actions.append(
            "Avoid structures, bridges, tunnels, or roads reported as damaged."
        )
        actions.append(
            "Expect possible aftershocks and check local inspection notices."
        )

    if any("volcano" in category for category in categories):
        actions.append(
            "Do not approach volcanic areas, lava, vents, ash clouds, "
            "or official exclusion zones."
        )
        actions.append(
            "Check the local geological observatory before travelling."
        )

    if any("wildfire" in category for category in categories):
        actions.append(
            "Move away from wildfire and smoke-affected areas early."
        )
        actions.append(
            "Check official evacuation zones and road closures."
        )

    if any(
        word in category
        for category in categories
        for word in ("flood", "rain")
    ):
        actions.append(
            "Do not drive or walk through floodwater."
        )
        actions.append(
            "Avoid low-lying roads, underpasses, and river crossings."
        )

    if any("wind" in category for category in categories):
        actions.append(
            "Avoid exposed areas, trees, scaffolding, and loose structures."
        )

    mobility_value = mobility.lower().strip()
    transport_value = transport.lower().strip()

    needs_set = {
        item.strip().lower()
        for item in needs.split(",")
        if item.strip()
    }

    if (
        "wheelchair" in mobility_value
        or "limited" in mobility_value
    ):
        actions.append(
            "Confirm that the shelter and destination have step-free access."
        )
        actions.append(
            "Arrange accessible transport before conditions worsen."
        )
        actions.append(
            "Carry a mobility-device charger, battery, repair kit, "
            "and essential accessories."
        )
        actions.append(
            "Allow additional evacuation time and avoid routes with stairs."
        )

    if needs_set.intersection(
        {"dog", "dogs", "pet", "pets", "cat", "cats"}
    ):
        actions.append(
            "Confirm a pet-friendly shelter before leaving."
        )
        actions.append(
            "Keep the dog on a leash or in a secure carrier during movement."
        )
        actions.append(
            "Pack pet identification, food, water, medication, "
            "waste bags, and vaccination information."
        )
        actions.append(
            "Do not leave the animal inside a parked vehicle."
        )

    if needs_set.intersection({"child", "children", "baby"}):
        actions.append(
            "Choose a clear family meeting point and keep children together."
        )
        actions.append(
            "Carry identification, emergency contacts, food, water, "
            "and child-specific supplies."
        )

    if needs_set.intersection(
        {"elderly", "senior", "older adult"}
    ):
        actions.append(
            "Allow additional preparation time and avoid long walking routes."
        )
        actions.append(
            "Keep medication, mobility aids, and emergency contacts ready."
        )

    if needs_set.intersection(
        {"medical", "medical_equipment", "oxygen", "medication"}
    ):
        actions.append(
            "Carry medication, medical documents, and backup power."
        )
        actions.append(
            "Identify a backup location that can support medical equipment."
        )

    if transport_value == "walking":
        actions.append(
            "Avoid long exposed walking routes and keep a nearby indoor option."
        )

    if transport_value == "public_transport":
        actions.append(
            "Check official service disruptions before starting the journey."
        )

    if transport_value == "car":
        actions.append(
            "Keep fuel or charge available and do not enter officially "
            "closed roads."
        )

    actions.append(
        "Official emergency authorities always override this generated plan."
    )

    # Remove duplicate actions while keeping their original order.
    return list(dict.fromkeys(actions))


@app.get("/plan")
async def create_plan(
    location: str = Query(
        ...,
        min_length=2,
        description="Current location or destination",
    ),
    mobility: str = Query(
        "standard",
        description="standard, wheelchair, or limited mobility",
    ),
    transport: str = Query(
        "car",
        description="car, walking, public_transport, or other",
    ),
    needs: str = Query(
        "",
        description="Comma-separated values such as dog,children,medical",
    ),
    risk_radius_km: int = Query(
        300,
        ge=25,
        le=1000,
    ),
) -> dict:
    async with httpx.AsyncClient(
        timeout=15,
        headers={
            "User-Agent": "SafeRoute-AI/1.2"
        },
    ) as client:
        resolved_location = await resolve_location(
            client,
            location,
        )

        latitude = resolved_location["latitude"]
        longitude = resolved_location["longitude"]

        weather_result, earthquake_result, event_result = (
            await asyncio.gather(
                fetch_weather(
                    client,
                    latitude,
                    longitude,
                ),
                fetch_earthquakes(
                    client,
                    latitude,
                    longitude,
                    risk_radius_km,
                ),
                fetch_natural_events(
                    client,
                    latitude,
                    longitude,
                    risk_radius_km,
                ),
                return_exceptions=True,
            )
        )

    hazards: list[dict] = []
    weather_snapshot: dict = {}

    source_status = {
        "weather": "available",
        "earthquakes": "available",
        "natural_events": "available",
    }

    if isinstance(weather_result, Exception):
        source_status["weather"] = "unavailable"
    else:
        weather_snapshot, weather_hazards = weather_result
        hazards.extend(weather_hazards)

    if isinstance(earthquake_result, Exception):
        source_status["earthquakes"] = "unavailable"
    else:
        hazards.extend(earthquake_result)

    if isinstance(event_result, Exception):
        source_status["natural_events"] = "unavailable"
    else:
        hazards.extend(event_result)

    hazards.sort(
        key=lambda hazard: (
            -hazard.get("severity", 0),
            hazard.get("distance_km", 999999),
        )
    )

    maximum_severity = max(
        (
            safe_float(hazard.get("severity"))
            for hazard in hazards
        ),
        default=0,
    )

    risk_score = min(
        100,
        int(
            sum(
                safe_float(hazard.get("severity")) * 8
                for hazard in hazards
            )
            + maximum_severity * 7
        ),
    )

    if maximum_severity >= 4:
        risk_level = "extreme"
        recommended_decision = (
            "follow_official_evacuation_guidance"
        )
    elif maximum_severity >= 3 or risk_score >= 45:
        risk_level = "high"
        recommended_decision = "delay_or_relocate"
    elif maximum_severity >= 2 or risk_score >= 20:
        risk_level = "moderate"
        recommended_decision = "modify_trip"
    else:
        risk_level = "low"
        recommended_decision = "continue_with_awareness"

    if hazards:
        top_hazard = hazards[0]

        summary = (
            f"Live feeds found {len(hazards)} relevant hazard signal"
            f"{'' if len(hazards) == 1 else 's'}. "
            f"Highest priority: {top_hazard['title']}. "
            f"{top_hazard['details']}"
        )
    else:
        summary = (
            "The connected feeds did not detect a major hazard near "
            "the selected location. Conditions can still change quickly."
        )

    personalized_actions = build_personalized_actions(
        hazards=hazards,
        risk_level=risk_level,
        mobility=mobility,
        transport=transport,
        needs=needs,
    )

    route_constraints = []

    for hazard in hazards:
        category = str(hazard.get("category", "")).lower()

        should_create_constraint = (
            hazard.get("type") == "natural_event"
            and hazard.get("severity", 0) >= 3
            and any(
                keyword in category
                for keyword in (
                    "volcano",
                    "wildfire",
                    "flood",
                    "landslide",
                    "storm",
                )
            )
        )

        if should_create_constraint:
            route_constraints.append({
                "type": "verify_or_avoid_area",
                "reason": hazard.get("title"),
                "center": {
                    "latitude": hazard.get("latitude"),
                    "longitude": hazard.get("longitude"),
                },
                "radius_km": (
                    50
                    if hazard.get("severity") == 4
                    else 25
                ),
                "warning": (
                    "Approximate hazard area. Verify official boundaries."
                ),
            })

    return {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "location": resolved_location,
        "traveler_profile": {
            "mobility": mobility,
            "transport": transport,
            "needs": [
                item.strip()
                for item in needs.split(",")
                if item.strip()
            ],
        },
        "assessment": {
            "score": risk_score,
            "risk_level": risk_level,
            "recommended_decision": recommended_decision,
            "summary": summary,
        },
        "weather": weather_snapshot,
        "hazards": hazards,
        "personalized_actions": personalized_actions,
        "route_constraints": route_constraints,
        "source_status": source_status,
        "limitations": [
            "Natural-event feeds may not show the full hazard boundary.",
            "Route constraints are approximate and are not confirmed closures.",
            "This service does not guarantee that any route is safe.",
            "Official emergency authorities always take priority.",
        ],
    }


@app.get("/skill-preview", response_class=HTMLResponse)
def skill_preview() -> str:
    return SKILL_PREVIEW_PAGE


@app.get("/skill.md", response_class=PlainTextResponse)
def skill_markdown() -> str:
    if not SKILL_FILE.exists():
        return (
            "# SafeRoute AI\n\n"
            "The SKILL.md file could not be found."
        )

    return SKILL_FILE.read_text(encoding="utf-8")
