# EpiAgent AIOps

## AI-Assisted Operational Intelligence & Incident Investigation

**From operational telemetry to actionable incident intelligence.**

EpiAgent AIOps is a working AI-assisted operational intelligence and incident-investigation application built on Splunk. It transforms Splunk-derived operational telemetry into system-health signals, rule-based anomalies, structured incidents, probable root-cause analysis, and actionable response recommendations.

The solution combines Splunk and SPL-based telemetry analysis, deterministic operational rules, specialized investigation agents, and Gemini-assisted interpretation while keeping operational decisions under human control.

**Core workflow:** Observe → Detect → Investigate → Diagnose → Respond

---

# Project Overview

Operations and engineering teams collect large volumes of logs and operational telemetry, but identifying meaningful signals, correlating incidents, investigating probable causes, and determining appropriate responses still requires significant interpretation.

EpiAgent AIOps addresses the gap between:

**Operational Telemetry → Operational Decision Intelligence**

Rather than replacing the observability platform with an LLM, the solution keeps **Splunk as the source of truth**, uses deterministic analysis for explainable operational signals, and applies Gemini where interpretation and recommendation add value.

---

# Business Problem

During operational incidents, engineers may need to:

- Review large volumes of telemetry
- Identify abnormal operational patterns
- Understand system health
- Correlate errors and incident evidence
- Investigate probable root causes
- Determine appropriate corrective actions
- Communicate operational findings clearly

Traditional observability platforms provide powerful telemetry and search capabilities, but operational teams still need to convert those signals into investigation context and decisions.

EpiAgent AIOps is designed to structure that workflow from detection through recommended response.

---

# Target Users

## Primary Users

- **SRE / Observability Teams** — operational health analysis and incident investigation
- **IT / Platform Operations** — system signals, incidents, probable causes, and response actions
- **Application Support / Operations** — application failures and operational troubleshooting

## Secondary Users

- **Engineering / Delivery Teams** — service-health and operational-risk visibility
- **Engineering Leadership** — higher-level operational health and incident context
- **Security / Access Operations** — investigation of the access-related signals supported by the implemented workflow

These are intended users based on the solution design and are not claims of customer adoption.

---

# Solution

EpiAgent AIOps integrates with Splunk Enterprise through the Splunk Python SDK and uses SPL queries to retrieve operational signals. Those signals are processed through deterministic operational logic and specialized agents for monitoring, anomaly detection, incident investigation, probable root-cause analysis, and response recommendations.

Gemini provides an additional interpretation layer for human-readable operational analysis and recommendations.

The product is designed as **AI-assisted operational decision support**, not autonomous infrastructure remediation.

---

# Implemented MVP Scope

The working implementation covers:

## Splunk Integration

- Splunk Enterprise as the observability foundation and source of truth
- Dedicated `epiagent` index for the demonstrated dataset
- Splunk Python SDK integration
- SPL-based operational queries

## Operational Monitoring

- Event-volume analysis
- HTTP status and server-error analysis
- Sourcetype visibility
- Deterministic system-health classification
- Incident scoring
- Operational summaries

## Rule-Based Anomaly Detection

- Traffic/source concentration analysis
- Elevated source activity detection
- Server-error burst detection
- Secure-access activity checks

## Incident Investigation

- Structured incident creation from operational evidence
- Severity, status, category, evidence, and ownership context
- Investigation views for operational analysis

## Probable Root Cause Analysis

- Correlation of incidents, anomalies, error context, source information, and system-health signals
- Rule-based probable-cause analysis
- Optional Gemini-assisted interpretation

## Response Recommendations

- Prioritized operational actions
- Suggested ownership
- Recommended investigation/remediation steps
- Expected outcome context

## AI-Assisted Interpretation

- Gemini-based incident interpretation
- Root-cause context
- Business-impact interpretation
- Recommended actions
- Confidence-oriented response format

## AI Fallback

- Core rule-based operational analysis remains available when Gemini is disabled or unavailable
- `AI_ENABLED` provides explicit control over AI usage

---

# Operational Workflow

```text
Operational Telemetry
        |
        v
Splunk Enterprise
        |
        v
SPL Analysis
        |
        v
Monitoring
        |
        v
Anomaly Detection
        |
        v
Incident Investigation
        |
        v
Probable Root Cause
        |
        v
Response Recommendations
        |
        v
Human Operations Decision
```

In short:

**Observe → Detect → Investigate → Diagnose → Respond**

---

# Architecture

![Architecture](docs/architecture.png)

## Architecture Philosophy

EpiAgent AIOps separates the operational workflow into distinct layers:

### 1. Splunk — Source of Truth

Splunk Enterprise stores and exposes the operational telemetry used by the application.

### 2. SPL + Deterministic Rules — Operational Intelligence

SPL queries retrieve relevant telemetry, while deterministic rules calculate and classify operational conditions such as system health, incident scores, error thresholds, and anomalies.

### 3. Specialized Agents — Investigation Workflow

Dedicated agents structure different stages of operational investigation.

### 4. Gemini — Interpretation Layer

Gemini interprets structured operational evidence and generates human-readable analysis and recommendations.

### 5. Human — Operational Decision

The system recommends actions but does not autonomously execute infrastructure remediation.

**Design principle:** Telemetry + Rules + Agents + Generative AI + Human Oversight

---

# Splunk Integration

EpiAgent AIOps uses Splunk Enterprise as the observability foundation. The demonstrated Splunk tutorial/sample logs are ingested into a dedicated index named `epiagent`.

The Python backend connects to Splunk using the Splunk SDK and executes SPL queries to derive operational signals including:

- Total event volume
- HTTP status distribution
- Sourcetype distribution
- HTTP 5xx/server-error activity
- Recent server-error evidence
- Operational patterns used by the investigation workflow

Splunk remains the authoritative telemetry source; Gemini is used as an interpretation layer rather than a replacement for observability analytics.

---

# AIOps Agent Workflow

Five specialized operational agents are implemented.

| Agent | Responsibility |
|---|---|
| **Monitoring Agent** | Operational health, event context, and monitoring summaries |
| **Anomaly Agent** | Rule-based detection of abnormal operational patterns |
| **Incident Agent** | Structured incident identification and investigation context |
| **Root Cause Agent** | Probable root-cause analysis using correlated operational evidence |
| **Response Agent** | Recommended operational actions and response guidance |

The agent workflow structures the operational investigation process while deterministic analysis and Splunk-derived evidence remain central to the system.

---

# Monitoring Agent

The Monitoring Agent provides operational context derived from Splunk and the deterministic Rule Engine.

Implemented outputs include:

- Total events
- Server-error types
- Total server errors
- System health
- Incident score
- Rule-based recommendation
- Error summary
- Top sourcetypes
- Splunk availability/status
- Optional Gemini-assisted summary

---

# Anomaly Detection Agent

The Anomaly Agent performs **rule-based anomaly detection** using Splunk-derived operational signals.

Implemented patterns include:

- High traffic/source concentration
- Elevated source activity
- Server-error bursts
- Elevated server-error activity
- Secure-access activity patterns

This implementation uses deterministic thresholds and should not be interpreted as a trained machine-learning anomaly-detection model.

---

# Incident Investigation Agent

The Incident Agent converts significant operational error patterns into structured incident information.

Incident context can include:

- Incident ID
- Title
- Severity
- Status
- Category
- Supporting evidence
- Owner

This provides a structured transition from operational signals to incident investigation.

---

# Probable Root Cause Analysis

The Root Cause Agent combines available operational context such as:

- Signal context
- Incidents
- Anomalies
- Event counts
- Server-error information
- Source information
- System-health context

The result is a **probable root-cause assessment**, supported by rule-based analysis and optional Gemini interpretation.

The project does not claim guaranteed causal determination.

---

# Response Recommendations

The Response Agent converts investigation findings into structured operational guidance.

Recommendations can include:

- Priority
- Owner
- Action
- Expected outcome

Depending on the investigated signal, recommendations can guide engineers toward areas such as backend health, application errors, recent deployments, capacity, upstream dependencies, access activity, or transaction-processing flows.

The application recommends actions; it does not autonomously execute remediation.

---

# AI Strategy

EpiAgent AIOps uses generative AI selectively rather than making the LLM responsible for core operational analysis.

## Deterministic Operational Intelligence

Splunk, SPL, and application rules handle measurable and explainable signals such as:

- Event counts
- HTTP/server errors
- Source concentration
- Threshold-based anomalies
- System health
- Incident scoring

## Generative AI

Gemini is used for higher-level interpretation such as:

- Severity interpretation
- Root-cause context
- Business-impact context
- Recommended action
- Human-readable operational summaries

## Human Oversight

Gemini output is advisory. Operations engineers retain responsibility for validating findings and deciding what action to take.

**AI principle:** Deterministic Operational Intelligence + Generative AI + Human Oversight

---

# AI Fallback & Resilience

A key design decision is that core operational analysis does not depend entirely on LLM availability.

The application supports an `AI_ENABLED` configuration flag.

When Gemini is disabled or unavailable:

**Splunk + SPL + Rule-Based Analysis + Operational Agents continue to provide core operational intelligence.**

When Gemini is available:

**Gemini adds interpretation and recommendation support on top of the structured operational evidence.**

This provides graceful degradation and keeps the deterministic operational workflow available independently of the generative-AI layer.

---

# Project Flow

![Project Flow](docs/project-flow.png)

---

# Technology & Integrations

| Technology | Purpose |
|---|---|
| **Splunk Enterprise 10.4.0** | Observability foundation used by the project |
| **SPL** | Operational telemetry querying and analysis |
| **Splunk Python SDK** | Application-to-Splunk integration |
| **Python** | Core application and operational logic |
| **Flask** | Web application/backend |
| **Gemini 2.5 Flash** | AI-assisted operational interpretation and recommendations |
| **Jinja2** | Dashboard/report templates |
| **HTML / CSS** | User-interface presentation |

---

# Product & Engineering Decisions

## Keep Splunk as the Source of Truth

The application builds on Splunk rather than attempting to replace the observability platform with an LLM.

## Separate Deterministic Analysis from Generative AI

Operational metrics, thresholds, health classification, and rule-based anomalies remain explainable and predictable. Gemini is used after structured evidence is available.

## Structure Investigation Through Specialized Agents

Monitoring, anomaly, incident, root-cause, and response responsibilities are separated into specialized components to create a clear investigation workflow.

## Support AI-Off Operation

The `AI_ENABLED` configuration allows core rule-based operational analysis to continue without Gemini.

## Keep Humans in the Response Loop

Response actions are recommendations. Infrastructure or application changes are not executed autonomously.

---

# Screenshots

## Operational Dashboard

![Operational Dashboard](docs/screenshots/dashboard.png)

## Monitoring Report

![Monitoring Report](docs/screenshots/monitoring-report.png)

## Investigation Hub

![Investigation Hub](docs/screenshots/investigation-hub.png)

## Anomaly Dashboard

![Anomaly Dashboard](docs/screenshots/anomaly-dashboard.png)

## Incident Dashboard

![Incident Dashboard](docs/screenshots/incident-dashboard.png)

## Root Cause Analysis

![Root Cause Analysis](docs/screenshots/root-cause-analysis.png)

## Recommended Actions

![Recommended Actions](docs/screenshots/recommended-actions.png)

---

# Project Structure

![Project Structure](docs/project-structure.png)

---

# Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

```env
SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=your_splunk_username
SPLUNK_PASSWORD=your_splunk_password
SPLUNK_INDEX=epiagent
AI_ENABLED=true
```

## Run Application

```bash
python app.py
```

---

# Demo Workflow

1. Start Splunk Enterprise
2. Ingest the demonstrated tutorial/sample logs
3. Run EpiAgent AIOps
4. Review operational monitoring and system-health context
5. Review detected rule-based anomalies
6. Investigate structured incidents
7. Review probable root-cause analysis
8. Review response recommendations
9. Review Gemini-assisted operational interpretation where AI is enabled
10. Use the dashboards to support the human operational decision

---

# Intended Business Value

EpiAgent AIOps is designed to support:

- Centralized operational intelligence
- Faster visibility into significant operational conditions
- Structured incident investigation
- Explainable rule-based anomaly detection
- Probable root-cause analysis
- Action-oriented response recommendations
- AI-assisted interpretation of operational evidence
- Reduced cognitive complexity when correlating multiple operational signals

These are intended product benefits. No quantified customer MTTR, MTTD, downtime reduction, ROI, adoption, or production-performance claims are made for this portfolio implementation.

---

# My Role & Contribution

**Role: End-to-End Product & Technical Lead**

I independently owned EpiAgent AIOps from problem definition through working implementation and project delivery.

## Product & AIOps

- Defined the operational problem and product concept
- Identified target users and operational use cases
- Defined and prioritized the MVP scope
- Designed the Observe → Detect → Investigate → Diagnose → Respond workflow
- Structured the monitoring, anomaly, incident, root-cause, and response capabilities

## AI Product Strategy

- Defined Gemini's role in the operational workflow
- Designed the boundary between deterministic operational intelligence and generative AI
- Designed the specialized agent workflow
- Implemented AI-enabled/AI-disabled operating modes
- Preserved human control over operational decisions and remediation

## Architecture & Engineering

- Designed the solution architecture
- Integrated the application with Splunk Enterprise
- Developed SPL-based operational data workflows
- Implemented deterministic operational rules
- Implemented the specialized operational agents
- Integrated Gemini for AI-assisted interpretation
- Developed the Flask/Jinja2 dashboard experience
- Integrated and validated the end-to-end investigation workflow

## Delivery

- Managed project scope and technical execution
- Built and integrated the working MVP
- Validated the operational workflow
- Prepared architecture, screenshots, and project documentation
- Completed the project demonstration/submission

---

# Challenges & Engineering Considerations

Key challenges addressed during the project included:

- Transforming raw observability data into structured operational intelligence
- Designing a staged incident-investigation workflow
- Integrating Python services with Splunk APIs and SDKs
- Developing SPL queries that provide meaningful operational signals
- Converting search results into structured agent inputs
- Separating deterministic operational analysis from generative-AI interpretation
- Maintaining useful core analysis when AI is disabled or unavailable
- Balancing implementation scope within a time-bounded project delivery

---

# Key Outcomes

The project delivered:

- A working AIOps MVP integrated with Splunk Enterprise
- Live SPL-based operational data retrieval
- Five specialized operational agents
- Deterministic monitoring and anomaly-analysis logic
- Structured incident-investigation workflow
- Probable root-cause analysis
- Action-oriented response recommendations
- Gemini-assisted operational interpretation
- AI-off fallback capability
- End-to-end operational intelligence dashboards

These are implementation outcomes, not claims of customer adoption or quantified production impact.

---

# Limitations

This portfolio implementation has deliberate boundaries:

- Analysis depends on the availability and quality of Splunk telemetry
- The demonstrated dataset uses Splunk tutorial/sample logs
- Anomaly detection is based on predefined rules and thresholds rather than a trained ML anomaly model
- Root-cause analysis identifies probable causes and does not guarantee causal determination
- Gemini output may require operational validation
- Gemini can be disabled or unavailable; core rule-based analysis remains available
- Response recommendations are not automatically executed
- No dedicated predictive service-degradation model or implemented Prediction Agent is claimed
- No quantified customer outcomes, production MTTR/MTTD improvements, or validated prediction-accuracy claims are made
- Enterprise-scale production controls are outside the demonstrated scope unless separately evidenced

---

# Future Scope — Not Implemented

Potential future evolution includes:

- Real-time streaming data support
- Advanced statistical or machine-learning anomaly detection
- Predictive service-degradation analysis
- Automated remediation workflows with appropriate controls
- Additional cloud and DevOps platform integrations
- Enterprise-scale observability support
- Multi-environment monitoring
- Operational copilots
- Extended autonomous decision-support capabilities

These items represent future possibilities and are **not part of the current implemented MVP**.

---

# Project Status

**Status: Working MVP / Portfolio Case Study**

EpiAgent AIOps demonstrates an end-to-end AI-assisted operational intelligence workflow combining:

**Splunk Telemetry + Deterministic Operational Analysis + Specialized Agents + Generative AI + Human Decision Support**

The project provides evidence of capability across:

- Technical Product Management
- AI Product Management
- Engineering Management
- AIOps
- Observability
- Incident Management
- Enterprise integration
- AI-assisted operational workflows
- Software architecture
- End-to-end technical delivery

