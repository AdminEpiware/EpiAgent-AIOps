# EpiAgent PMO

### AI-Assisted Project Governance & Portfolio Risk Intelligence

**From project execution data to explainable risk intelligence and AI-assisted management decisions.**

> Software projects don't fail because teams stop working. They fail because risks stay invisible until it's too late.

---

## Project Overview

**EpiAgent PMO** is a working AI-assisted project governance and portfolio risk-management application that transforms GitLab project execution data into project-health visibility, explainable risk signals, and Gemini-powered management recommendations.

The solution combines deterministic project-risk analytics with generative AI to support project and portfolio decision-making. Rather than using an LLM for every task, EpiAgent PMO separates explainable risk calculation from AI-assisted interpretation and keeps the final management decision with the human user.

**Core workflow:** GitLab → Project Metrics → Deterministic Risk Engine → Gemini → Management Decision Support

---

## Business Problem

Project execution information can be distributed across issues, work status, blockers, critical tasks, and other delivery activity. Project and portfolio managers still need to interpret this information to understand delivery health, identify risks, communicate status, and determine corrective actions.

Traditional dashboards provide visibility, but visibility alone does not automatically create management intelligence.

EpiAgent PMO addresses the gap between:

**Project Execution Data → Management Decision Intelligence**

The product is designed to help managers:

* Consolidate project and portfolio health visibility
* Identify blocked and critical work
* Assess delivery risk consistently
* Interpret project-health signals
* Generate management-oriented recommendations
* Support faster, better-informed project decisions

---

## Target Users

### Primary Users

* **PMO / Portfolio Managers** — portfolio-level project health and risk visibility
* **Project / Program Managers** — project-level health, blockers, critical issues, and decision support

### Secondary Users

* **Engineering / Delivery Managers** — software-delivery health and execution-risk visibility
* **Leadership / Management** — concise project-health information and executive-oriented recommendations

These are intended users based on the implemented solution design; they are not claims of customer adoption.

---

## Solution

EpiAgent PMO connects to GitLab project data, calculates project and portfolio metrics, applies deterministic risk logic, and uses Gemini to interpret structured risk signals and generate management-oriented recommendations.

The application provides:

* Portfolio-level project visibility
* Project-level delivery-health metrics
* Explainable risk scoring
* Green / Yellow / Red health classification
* Blocked and critical issue visibility
* Gemini-powered executive recommendations
* Management-oriented dashboard and report presentation

The product is designed as **AI-assisted decision support**, not autonomous project management.

---

## Implemented MVP Scope

The working implementation covers the following capabilities:

### Portfolio Management

* Retrieves GitLab group projects dynamically
* Provides portfolio-level project visibility
* Surfaces at-risk projects and critical blockers
* Presents overall portfolio health

### Project Health

* Retrieves project issue data
* Calculates project execution metrics
* Displays completion, in-progress, blocked, and critical work
* Presents project health and risk score

### Risk Intelligence

* Applies deterministic risk rules
* Produces a risk score from 0–100
* Classifies project health as Green, Yellow, or Red

### AI Decision Support

* Sends structured project-health metrics to Gemini
* Generates executive-oriented project interpretation
* Identifies key risks
* Recommends management actions
* Provides delay assessment and PMO decision support

### Delivery & Deployment

* FastAPI-based application
* Jinja2-based dashboard/report presentation
* Docker containerization
* Google Cloud Run deployment target

---

## Product Workflow

```text
GitLab Projects & Issues
          |
          v
GitLab REST API
          |
          v
Portfolio / Project Metrics
          |
          v
Deterministic Risk Engine
          |
          v
Risk Score + Health Classification
          |
          v
Gemini AI Analysis
          |
          v
Executive Risks + Recommended Actions
          |
          v
Human Management Decision
```

In short:

**Data → Metrics → Risk → AI → Decision**

---

## AI Strategy

EpiAgent PMO uses a hybrid decision-support architecture rather than relying entirely on generative AI.

### 1. Deterministic Analytics

Predictable and explainable calculations are handled by application logic:

* Project metrics
* Completion rate
* Blocked and critical issue counts
* Risk score
* Project-health classification

### 2. Generative AI

Gemini is used where interpretation and synthesis add value:

* Executive summary generation
* Risk interpretation
* Recommended actions
* Delay assessment
* PMO decision support

### 3. Human Oversight

Gemini recommendations are advisory. The application does not autonomously execute project-management decisions. Final judgment and action remain with the manager.

**AI design principle:** Explainable Analytics + Generative AI + Human Oversight

---

## Risk Engine

The deterministic Risk Engine converts project execution signals into an explainable risk score.

Implemented risk logic includes:

* Completion below 50% → +20 risk
* Each blocked issue → +25 risk
* Each critical issue → +20 risk
* Maximum risk score → 100

### Health Classification

| Risk Score | Health Status |
|---:|---|
| 0–39 | Green |
| 40–69 | Yellow |
| 70–100 | Red |

Completion percentage is calculated as:

`Completed Tasks / Total Tasks × 100`

The deterministic risk layer establishes consistent project-health signals before Gemini performs management-oriented interpretation.

---

## System Architecture

![EpiAgent PMO Architecture](docs/architecture.png)

### Architecture Flow

```text
GitLab Projects
      |
      v
GitLab REST API
      |
      v
EpiAgent PMO / FastAPI
      |
      +-------------------------+
      |                         |
      v                         v
Portfolio & Project       Deterministic
Metrics                   Risk Engine
      |                         |
      +------------+------------+
                   |
                   v
          Project Health Context
                   |
                   v
             Gemini 2.5 Flash
                   |
                   v
       AI Executive Recommendation
                   |
                   v
       Dashboard / Report Experience
```

The application is containerized with Docker and designed for deployment to Google Cloud Run.

---

## Technology & Integrations

| Technology | Purpose |
|---|---|
| **Python** | Primary application implementation |
| **FastAPI** | Application/backend and request workflow |
| **GitLab REST API** | Project and issue data integration |
| **Gemini 2.5 Flash** | AI interpretation and management recommendations |
| **Jinja2** | Dashboard and report rendering |
| **Docker** | Application containerization |
| **Google Cloud Run** | Cloud deployment target |

---

## Product & Engineering Decisions

### Use Live Project Data

GitLab integration allows the application to derive portfolio and project context from project execution data instead of relying only on manually entered information.

### Separate Risk Calculation from Generative AI

Risk scoring and health classification use deterministic logic so that core project-health signals remain predictable and explainable.

Gemini is applied after those signals are calculated, where natural-language interpretation and recommendation generation provide greater value.

### Keep Humans in the Decision Loop

The application provides recommendations rather than automatically executing project-management actions. This preserves management oversight over delivery decisions.

### Modular Application Structure

The implementation separates external integration, portfolio aggregation, risk logic, AI recommendation generation, dashboard orchestration, and report presentation into distinct application components.

---

## Portfolio Dashboard

The portfolio dashboard provides portfolio-wide visibility into project health and delivery risk.

![Portfolio Dashboard](docs/portfolio.png)

Key information includes:

* Total projects
* At-risk projects
* Critical blockers
* Overall portfolio health

---

## Project Dashboard

The project dashboard provides detailed project-level execution and risk visibility.

![Project Dashboard](docs/project-dashboard.png)

Key information includes:

* Project health
* Risk score
* Total tasks
* Completion percentage
* In-progress work
* Blocked tasks
* Critical issues
* AI-assisted executive recommendation

---

## Demo

**EpiAgent PMO — Working Demo**

https://www.youtube.com/watch?v=Bzs7Tcqk5vQ

### Demo Flow

1. Open the Portfolio Dashboard
2. Review portfolio health
3. Select a project
4. Open the Project Dashboard
5. Review project metrics, risk score, and health
6. Review management-oriented project information
7. Review AI-assisted recommendations

---

## Intended Business Value

EpiAgent PMO is designed to support:

* Centralized portfolio and project-health visibility
* Earlier visibility into blocked and critical work
* Consistent and explainable delivery-risk assessment
* AI-assisted interpretation of project-health signals
* Management-oriented corrective-action recommendations
* Better-informed project and portfolio decision workflows

These are intended product benefits. No quantified customer ROI, adoption, or production performance claims are made for this portfolio implementation.

---

## My Role & Contribution

**Role: End-to-End Product & Technical Lead**

I independently owned EpiAgent PMO from problem definition through working implementation and delivery.

### Product & Project

* Defined the project-governance problem and product concept
* Identified target management workflows and users
* Defined and prioritized the MVP scope
* Designed the portfolio and project decision-support workflow
* Managed the project end-to-end through delivery and demonstration

### AI Product Strategy

* Defined the AI use case and recommendation workflow
* Designed the boundary between deterministic risk analytics and generative AI
* Integrated Gemini into the management decision-support workflow
* Kept final project-management decisions under human oversight

### Architecture & Engineering

* Designed the solution architecture
* Implemented the application and service components
* Integrated GitLab project and issue data
* Implemented deterministic risk-analysis logic
* Integrated Gemini for executive recommendations
* Developed portfolio and project dashboard workflows
* Containerized the application with Docker
* Prepared the application for Google Cloud Run deployment

### Delivery

* Managed scope and technical execution
* Integrated and validated the end-to-end workflow
* Prepared project documentation and technical evidence
* Produced the working demonstration
* Completed the project delivery/submission

---

## Limitations

This portfolio implementation has deliberate boundaries:

* Project-health analysis depends on the quality and completeness of available GitLab project/issue data
* Risk weights are predefined deterministic rules
* Gemini recommendations are advisory and may require management validation
* The application does not autonomously execute project-management actions
* No customer adoption, quantified ROI, or validated prediction-accuracy claims are made
* Comprehensive enterprise controls such as organization-wide SSO/RBAC, formal compliance controls, and production-scale operational governance are outside the demonstrated scope unless otherwise evidenced

---

## Future Scope — Not Implemented

Potential future evolution includes:

* Cross-project risk correlation
* Resource forecasting
* Budget risk analysis
* Broader portfolio governance
* Multi-project risk intelligence
* Extended executive decision support
* More advanced project-governance automation

These items represent future possibilities and are **not part of the current implemented MVP**.

---

## Project Status

**Status: Working MVP / Portfolio Case Study**

EpiAgent PMO demonstrates an end-to-end AI-assisted project-governance workflow combining:

**Enterprise Project Data + Explainable Risk Analytics + Generative AI + Management Decision Support**

The project is presented as evidence of capability across:

* AI Product Management
* Product Management
* Project / Portfolio Management
* Product Ownership
* AI-assisted enterprise software
* Software architecture
* Engineering and technical delivery
* Enterprise integration
* End-to-end product execution

---

## Repository

This repository contains the working EpiAgent PMO implementation, architecture evidence, dashboard screenshots, deployment configuration, and supporting documentation.

