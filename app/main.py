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

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="SafeRoute AI provides personalized disaster-aware travel guidance."
    >

    <title>SafeRoute AI</title>

    <style>
        :root {
            --background: #07111f;
            --surface: rgba(15, 31, 50, 0.82);
            --surface-light: rgba(26, 48, 72, 0.72);
            --border: rgba(148, 180, 209, 0.17);
            --text: #f4f8fc;
            --muted: #a8bbcc;
            --green: #5ee6b8;
            --blue: #62a9ff;
            --yellow: #ffd46a;
            --orange: #ff9e64;
            --red: #ff6b7d;
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
            color: var(--text);
            background:
                radial-gradient(
                    circle at 15% 10%,
                    rgba(65, 155, 255, 0.22),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 85% 30%,
                    rgba(45, 214, 158, 0.14),
                    transparent 28%
                ),
                var(--background);
        }

        a {
            color: inherit;
        }

        .container {
            width: min(1140px, calc(100% - 36px));
            margin: 0 auto;
        }

        nav {
            position: sticky;
            top: 0;
            z-index: 20;
            border-bottom: 1px solid var(--border);
            background: rgba(7, 17, 31, 0.83);
            backdrop-filter: blur(18px);
        }

        .nav-inner {
            min-height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 11px;
            font-weight: 800;
            letter-spacing: -0.03em;
            text-decoration: none;
        }

        .logo {
            width: 38px;
            height: 38px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(94, 230, 184, 0.35);
            border-radius: 12px;
            background: rgba(94, 230, 184, 0.1);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 18px;
        }

        .nav-links a {
            color: var(--muted);
            text-decoration: none;
            font-size: 14px;
        }

        .nav-links a:hover {
            color: var(--text);
        }

        .hero {
            padding: 100px 0 70px;
            text-align: center;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 13px;
            border: 1px solid rgba(94, 230, 184, 0.25);
            border-radius: 999px;
            color: var(--green);
            background: rgba(94, 230, 184, 0.07);
            font-size: 13px;
            font-weight: 700;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 16px var(--green);
        }

        h1 {
            max-width: 880px;
            margin: 28px auto 22px;
            font-size: clamp(48px, 8vw, 88px);
            line-height: 0.98;
            letter-spacing: -0.065em;
        }

        .gradient-text {
            background: linear-gradient(
                105deg,
                #ffffff 15%,
                #7cb8ff 50%,
                #5ee6b8 92%
            );
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero-description {
            max-width: 720px;
            margin: 0 auto;
            color: var(--muted);
            font-size: clamp(17px, 2vw, 21px);
            line-height: 1.7;
        }

        .hero-actions {
            margin-top: 34px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 9px;
            min-height: 48px;
            padding: 0 20px;
            border: 1px solid var(--border);
            border-radius: 12px;
            font-weight: 750;
            text-decoration: none;
            transition:
                transform 150ms ease,
                border-color 150ms ease,
                background 150ms ease;
        }

        .button:hover {
            transform: translateY(-2px);
        }

        .button-primary {
            color: #06141d;
            border-color: transparent;
            background: linear-gradient(135deg, var(--green), #78baff);
        }

        .button-secondary {
            color: var(--text);
            background: rgba(255, 255, 255, 0.045);
        }

        section {
            padding: 70px 0;
        }

        .section-heading {
            max-width: 700px;
            margin-bottom: 34px;
        }

        .eyebrow {
            margin: 0 0 10px;
            color: var(--green);
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        h2 {
            margin: 0;
            font-size: clamp(32px, 5vw, 50px);
            letter-spacing: -0.045em;
        }

        .section-heading p {
            margin-top: 14px;
            color: var(--muted);
            font-size: 17px;
            line-height: 1.7;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }

        .card {
            padding: 23px;
            border: 1px solid var(--border);
            border-radius: 18px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.055),
                    rgba(255, 255, 255, 0.018)
                );
            box-shadow: 0 20px 70px rgba(0, 0, 0, 0.14);
        }

        .card-icon {
            width: 46px;
            height: 46px;
            display: grid;
            place-items: center;
            margin-bottom: 18px;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: var(--surface-light);
            font-size: 23px;
        }

        .card h3 {
            margin: 0 0 8px;
            font-size: 18px;
        }

        .card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.6;
            font-size: 14px;
        }

        .workflow {
            display: grid;
            grid-template-columns:
                minmax(130px, 1fr)
                auto
                minmax(130px, 1fr)
                auto
                minmax(130px, 1fr)
                auto
                minmax(130px, 1fr);
            align-items: center;
            gap: 12px;
        }

        .workflow-step {
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: 17px;
            background: var(--surface);
            text-align: center;
        }

        .step-number {
            width: 30px;
            height: 30px;
            display: grid;
            place-items: center;
            margin: 0 auto 12px;
            border-radius: 50%;
            color: #07111f;
            background: var(--green);
            font-size: 13px;
            font-weight: 900;
        }

        .workflow-step strong {
            font-size: 15px;
        }

        .workflow-step span {
            margin-top: 7px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.5;
        }

        .arrow {
            color: var(--blue);
            font-size: 24px;
        }

        .risk-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }

        .risk-card {
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: var(--surface);
        }

        .risk-level {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 9px;
            font-weight: 800;
        }

        .risk-dot {
            width: 11px;
            height: 11px;
            border-radius: 50%;
        }

        .low {
            background: var(--green);
        }

        .moderate {
            background: var(--yellow);
        }

        .high {
            background: var(--orange);
        }

        .extreme {
            background: var(--red);
        }

        .risk-card p {
            margin: 0;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.55;
        }

        .planner {
            display: grid;
            grid-template-columns: 0.9fr 1.1fr;
            gap: 18px;
        }

        form,
        .result-panel {
            padding: 26px;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: var(--surface);
        }

        .form-row {
            margin-bottom: 16px;
        }

        label {
            display: block;
            margin-bottom: 7px;
            color: #dce9f4;
            font-size: 13px;
            font-weight: 750;
        }

        input,
        select {
            width: 100%;
            min-height: 45px;
            padding: 0 13px;
            border: 1px solid var(--border);
            border-radius: 11px;
            outline: none;
            color: var(--text);
            background: rgba(4, 13, 23, 0.72);
            font: inherit;
        }

        input:focus,
        select:focus {
            border-color: var(--blue);
        }

        select option {
            color: #111827;
        }

        button {
            width: 100%;
            min-height: 48px;
            border: 0;
            border-radius: 12px;
            color: #06141d;
            background: linear-gradient(135deg, var(--green), var(--blue));
            font: inherit;
            font-weight: 850;
            cursor: pointer;
        }

        button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        .result-panel {
            min-height: 100%;
        }

        .result-placeholder {
            min-height: 330px;
            display: grid;
            place-items: center;
            padding: 30px;
            border: 1px dashed var(--border);
            border-radius: 14px;
            color: var(--muted);
            text-align: center;
        }

        .result-content {
            display: none;
        }

        .result-risk {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            padding: 7px 11px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.04);
            font-size: 13px;
            font-weight: 800;
        }

        .action-list {
            padding-left: 19px;
            color: var(--muted);
        }

        .action-list li {
            margin-bottom: 9px;
            line-height: 1.5;
        }

        .prototype-note {
            margin-top: 50px;
            padding: 18px 20px;
            border: 1px solid rgba(255, 212, 106, 0.22);
            border-radius: 14px;
            color: #f5d98c;
            background: rgba(255, 212, 106, 0.07);
            line-height: 1.6;
        }

        footer {
            padding: 40px 0 55px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 14px;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }

        @media (max-width: 900px) {
            .grid,
            .risk-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .workflow {
                grid-template-columns: 1fr;
            }

            .arrow {
                transform: rotate(90deg);
                text-align: center;
            }

            .planner {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 620px) {
            .nav-links a:not(.button) {
                display: none;
            }

            .hero {
                padding-top: 72px;
            }

            .grid,
            .risk-grid {
                grid-template-columns: 1fr;
            }

            .container {
                width: min(100% - 24px, 1140px);
            }
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
                <a href="#capabilities">Capabilities</a>
                <a href="#workflow">Workflow</a>
                <a href="#planner">Try it</a>
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
                    NANDA-compatible safety service
                </div>

                <h1>
                    Travel decisions built for
                    <span class="gradient-text">changing conditions.</span>
                </h1>

                <p class="hero-description">
                    SafeRoute AI turns a traveler’s location, transport,
                    accessibility requirements and emergency needs into a
                    clear, personalized action plan.
                </p>

                <div class="hero-actions">
                    <a class="button button-primary" href="#planner">
                        Generate a safety plan
                    </a>

                    <a class="button button-secondary" href="/skill-preview">
                        View SkillMD
                    </a>

                    <a class="button button-secondary" href="/docs">
                        API documentation
                    </a>
                </div>
            </div>
        </section>

        <section id="capabilities">
            <div class="container">
                <div class="section-heading">
                    <p class="eyebrow">Hazard intelligence</p>
                    <h2>One plan, built around the traveler.</h2>

                    <p>
                        The system combines travel context and emergency needs
                        so an agent can provide more useful guidance than a
                        generic alert.
                    </p>
                </div>

                <div class="grid">
                    <article class="card">
                        <div class="card-icon">🌧️</div>
                        <h3>Severe weather</h3>
                        <p>
                            Adapt outdoor activities, timing and transport
                            during rain, snow and storms.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">🌊</div>
                        <h3>Flood awareness</h3>
                        <p>
                            Highlight low-lying areas and advise travelers to
                            follow verified closure information.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">🌎</div>
                        <h3>Earthquake context</h3>
                        <p>
                            Help travelers avoid potentially damaged
                            infrastructure and monitor official alerts.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">🌋</div>
                        <h3>Volcanoes and lava</h3>
                        <p>
                            Direct travelers toward official exclusion zones
                            and geological authority guidance.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">🔥</div>
                        <h3>Wildfires</h3>
                        <p>
                            Prioritize relocation, official evacuation zones
                            and reduced exposure to smoke.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">♿</div>
                        <h3>Accessibility</h3>
                        <p>
                            Include step-free transport, accessible shelter
                            and extra evacuation time.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">👨‍👩‍👧</div>
                        <h3>Family planning</h3>
                        <p>
                            Create meeting-point, child, elderly-traveler and
                            pet-specific recommendations.
                        </p>
                    </article>

                    <article class="card">
                        <div class="card-icon">🩺</div>
                        <h3>Medical needs</h3>
                        <p>
                            Remind travelers about medication, emergency
                            contacts and backup power.
                        </p>
                    </article>
                </div>
            </div>
        </section>

        <section id="workflow">
            <div class="container">
                <div class="section-heading">
                    <p class="eyebrow">Decision workflow</p>
                    <h2>From a question to an action plan.</h2>
                </div>

                <div class="workflow">
                    <div class="workflow-step">
                        <span class="step-number">1</span>
                        <strong>Collect context</strong>
                        <span>
                            Location, transportation and accessibility needs
                        </span>
                    </div>

                    <div class="arrow">→</div>

                    <div class="workflow-step">
                        <span class="step-number">2</span>
                        <strong>Assess the request</strong>
                        <span>
                            Identify relevant traveler and emergency factors
                        </span>
                    </div>

                    <div class="arrow">→</div>

                    <div class="workflow-step">
                        <span class="step-number">3</span>
                        <strong>Generate actions</strong>
                        <span>
                            Return prioritized personalized recommendations
                        </span>
                    </div>

                    <div class="arrow">→</div>

                    <div class="workflow-step">
                        <span class="step-number">4</span>
                        <strong>Follow authorities</strong>
                        <span>
                            Official emergency instructions remain primary
                        </span>
                    </div>
                </div>
            </div>
        </section>

        <section>
            <div class="container">
                <div class="section-heading">
                    <p class="eyebrow">Risk communication</p>
                    <h2>Clear levels. Clear actions.</h2>
                </div>

                <div class="risk-grid">
                    <div class="risk-card">
                        <div class="risk-level">
                            <span class="risk-dot low"></span>
                            Low
                        </div>

                        <p>
                            Continue with awareness and monitor official
                            conditions.
                        </p>
                    </div>

                    <div class="risk-card">
                        <div class="risk-level">
                            <span class="risk-dot moderate"></span>
                            Moderate
                        </div>

                        <p>
                            Modify activities, timing, transportation or route.
                        </p>
                    </div>

                    <div class="risk-card">
                        <div class="risk-level">
                            <span class="risk-dot high"></span>
                            High
                        </div>

                        <p>
                            Delay, relocate or substantially change the trip.
                        </p>
                    </div>

                    <div class="risk-card">
                        <div class="risk-level">
                            <span class="risk-dot extreme"></span>
                            Extreme
                        </div>

                        <p>
                            Follow official evacuation or shelter guidance.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <section id="planner">
            <div class="container">
                <div class="section-heading">
                    <p class="eyebrow">Live prototype</p>
                    <h2>Generate a personalized plan.</h2>

                    <p>
                        Enter traveler information to test the current
                        SafeRoute decision-support endpoint.
                    </p>
                </div>

                <div class="planner">
                    <form id="planner-form">
                        <div class="form-row">
                            <label for="location">Location or destination</label>

                            <input
                                id="location"
                                name="location"
                                value="Naples"
                                minlength="2"
                                required
                            >
                        </div>

                        <div class="form-row">
                            <label for="mobility">Mobility requirement</label>

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
                            <label for="needs">
                                Additional needs
                            </label>

                            <input
                                id="needs"
                                name="needs"
                                placeholder="children,pets,medical,elderly"
                                value="children,pets"
                            >
                        </div>

                        <button id="submit-button" type="submit">
                            Generate safety plan
                        </button>
                    </form>

                    <div class="result-panel">
                        <div
                            id="result-placeholder"
                            class="result-placeholder"
                        >
                            Your personalized safety plan will appear here.
                        </div>

                        <div id="result-content" class="result-content">
                            <div id="result-risk" class="result-risk"></div>

                            <h3 id="result-decision"></h3>

                            <p id="result-summary"></p>

                            <h4>Personalized actions</h4>

                            <ul
                                id="result-actions"
                                class="action-list"
                            ></ul>
                        </div>
                    </div>
                </div>

                <div class="prototype-note">
                    <strong>Prototype notice:</strong>
                    the deployed version currently generates personalized
                    guidance from traveler inputs. Live weather, earthquake,
                    wildfire and volcanic feeds are not connected yet.
                    Official emergency instructions always take priority.
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
        const placeholder = document.getElementById("result-placeholder");
        const resultContent = document.getElementById("result-content");
        const resultRisk = document.getElementById("result-risk");
        const resultDecision = document.getElementById("result-decision");
        const resultSummary = document.getElementById("result-summary");
        const resultActions = document.getElementById("result-actions");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            submitButton.disabled = true;
            submitButton.textContent = "Generating...";

            const formData = new FormData(form);
            const params = new URLSearchParams();

            params.set("location", formData.get("location"));
            params.set("mobility", formData.get("mobility"));
            params.set("transport", formData.get("transport"));
            params.set("needs", formData.get("needs"));

            try {
                const response = await fetch(`/plan?${params.toString()}`);

                if (!response.ok) {
                    throw new Error("The plan could not be generated.");
                }

                const data = await response.json();

                placeholder.style.display = "none";
                resultContent.style.display = "block";

                const riskLevel =
                    data.assessment?.risk_level ?? "unknown";

                resultRisk.textContent =
                    `Risk level: ${riskLevel.toUpperCase()}`;

                resultDecision.textContent =
                    data.assessment?.recommended_decision
                    ?.replaceAll("_", " ")
                    ?? "Continue with awareness";

                resultSummary.textContent =
                    data.assessment?.summary
                    ?? "No summary was returned.";

                resultActions.innerHTML = "";

                for (const action of data.personalized_actions ?? []) {
                    const item = document.createElement("li");
                    item.textContent = action;
                    resultActions.appendChild(item);
                }
            } catch (error) {
                placeholder.style.display = "grid";
                placeholder.textContent = error.message;
                resultContent.style.display = "none";
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Generate safety plan";
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
        description="Comma-separated needs",
    ),
) -> dict:
    actions = [
        "Monitor official emergency alerts for the selected location.",
        "Keep identification, water, medication and a charged phone available.",
        "Do not use routes that local authorities have closed.",
    ]

    mobility_lower = mobility.lower()
    transport_lower = transport.lower()
    needs_lower = needs.lower()

    if (
        "wheelchair" in mobility_lower
        or "limited" in mobility_lower
    ):
        actions.append(
            "Confirm step-free transportation and accessible shelter options."
        )

    if "medical" in needs_lower:
        actions.append(
            "Carry medication, backup power and emergency medical contacts."
        )

    if "children" in needs_lower:
        actions.append(
            "Choose a family meeting point and keep emergency contacts ready."
        )

    if "pets" in needs_lower:
        actions.append(
            "Confirm pet-friendly shelter and transportation options."
        )

    if "elderly" in needs_lower:
        actions.append(
            "Allow additional evacuation time and avoid long walking routes."
        )

    if transport_lower == "walking":
        actions.append(
            "Avoid long exposed walking routes during severe conditions."
        )

    if transport_lower == "public_transport":
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
