import os
from flask import Flask, render_template
from dotenv import load_dotenv
from agents.monitoring_agent import MonitoringAgent
from agents.incident_agent import IncidentAgent
from agents.anomaly_agent import AnomalyAgent
from agents.rootcause_agent import RootCauseAgent
from agents.response_agent import ResponseAgent

load_dotenv()

app = Flask(__name__)

AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"


SIGNALS = {
    "web-traffic": {
        "id": "web-traffic",
        "name": "Web Traffic Observability",
        "short_name": "Web Traffic",
        "description": "HTTP access logs, request patterns, and server-side errors",
        "investigation_title": "Web Traffic Investigation",
        "monitoring_focus": "HTTP access logs, request volume, status codes, and web/server-side error patterns",
        "anomaly_focus": "Traffic spikes, elevated source activity, and web request concentration",
        "incident_focus": "HTTP 500, 503, and 505 server-side incidents",
    },
    "security-access": {
        "id": "security-access",
        "name": "Security & Access Logs",
        "short_name": "Security Access",
        "description": "Secure access events and authentication-related operational signals",
        "investigation_title": "Security & Access Investigation",
        "monitoring_focus": "Secure access logs, authentication activity, and access-related operational signals",
        "anomaly_focus": "Authentication surge, abnormal secure access activity, and unusual access volume",
        "incident_focus": "Security or access-related incidents derived from authentication/access patterns",
    },
    "business-transactions": {
        "id": "business-transactions",
        "name": "Business Transaction Logs",
        "short_name": "Business Transactions",
        "description": "Vendor sales activity and transaction monitoring",
        "investigation_title": "Business Transaction Investigation",
        "monitoring_focus": "Vendor sales logs, transaction activity, and business process signals",
        "anomaly_focus": "Transaction volume changes, vendor activity concentration, and business signal deviation",
        "incident_focus": "Business transaction failures or transaction-impacting operational incidents",
    },
}


def get_signal(signal_id):
    return SIGNALS.get(signal_id, SIGNALS["web-traffic"])


def source_matches_signal(source, signal_id):
    sourcetype = source.get("sourcetype", "").lower()

    if signal_id == "web-traffic":
        return "www" in sourcetype or "access" in sourcetype

    if signal_id == "security-access":
        return "secure" in sourcetype or "access" in sourcetype

    if signal_id == "business-transactions":
        return "vendor" in sourcetype or "sales" in sourcetype

    return False


def calculate_signal_event_count(data, signal_id):
    sources = data.get("sources", [])
    return sum(
        int(source.get("count", 0))
        for source in sources
        if source_matches_signal(source, signal_id)
    )


def calculate_signal_health_and_score(event_count, error_count=0):
    if error_count > 5000:
        return "RED", 95

    if error_count > 1000:
        return "WARNING", 70

    if event_count > 35000:
        return "WARNING", 65

    if event_count > 0:
        return "GREEN", 20

    return "UNKNOWN", 0


def build_systems(data):
    systems = []

    for signal_id, signal in SIGNALS.items():
        event_count = calculate_signal_event_count(data, signal_id)

        if signal_id == "web-traffic":
            error_count = data.get("total_server_errors", 0)
        else:
            error_count = 0

        health, risk_score = calculate_signal_health_and_score(
            event_count=event_count,
            error_count=error_count
        )

        systems.append({
            "id": signal_id,
            "name": signal["name"],
            "description": signal["description"],
            "health": health,
            "risk_score": risk_score,
            "errors": error_count,
            "events": event_count,
        })

    return systems


def get_signal_recommendation(signal_id, data):
    total_server_errors = data.get("total_server_errors", 0)
    event_count = calculate_signal_event_count(data, signal_id)

    if signal_id == "web-traffic":
        if total_server_errors > 1000:
            return (
                "Rule-based analysis from live Splunk data detected elevated HTTP 5xx errors. "
                "Review affected backend services, recent deployments, and dependency health."
            )
        return (
            "Rule-based analysis from live Splunk data indicates web traffic is currently stable. "
            "Continue monitoring HTTP status trends and traffic concentration."
        )

    if signal_id == "security-access":
        if event_count > 30000:
            return (
                "Rule-based analysis from live Splunk data detected high secure access activity. "
                "Review authentication trends, access source patterns, and identity provider health."
            )
        return (
            "Rule-based analysis from live Splunk data indicates secure access activity is within expected range."
        )

    if signal_id == "business-transactions":
        if event_count > 25000:
            return (
                "Rule-based analysis from live Splunk data detected significant business transaction activity. "
                "Review vendor transaction flow, processing queues, and integration health."
            )
        return (
            "Rule-based analysis from live Splunk data indicates business transaction signals are currently stable."
        )

    return "Rule-based analysis from live Splunk data is active."


def filter_monitoring_data(data, signal_id):
    filtered_data = dict(data)

    filtered_sources = [
        source for source in data.get("sources", [])
        if source_matches_signal(source, signal_id)
    ]

    filtered_data["sources"] = filtered_sources
    filtered_data["signal_event_count"] = sum(
        int(source.get("count", 0)) for source in filtered_sources
    )

    if signal_id == "web-traffic":
        filtered_data["errors"] = [
            error for error in data.get("errors", [])
            if "http" in error.lower() or "500" in error or "503" in error or "505" in error
        ]
        filtered_data["total_server_errors"] = data.get("total_server_errors", 0)
    else:
        filtered_data["errors"] = []
        filtered_data["total_server_errors"] = 0

    health, score = calculate_signal_health_and_score(
        event_count=filtered_data["signal_event_count"],
        error_count=filtered_data["total_server_errors"]
    )

    filtered_data["health"] = health
    filtered_data["score"] = score
    filtered_data["recommendation"] = get_signal_recommendation(signal_id, data)

    return filtered_data


def filter_incident_data(incident_data, signal_id):
    incidents = incident_data.get("incidents", [])

    if signal_id == "web-traffic":
        filtered_incidents = [
            incident for incident in incidents
            if incident["category"] in ["Application", "Availability", "Protocol"]
        ]

    elif signal_id == "security-access":
        filtered_incidents = [
            incident for incident in incidents
            if "security" in incident["category"].lower()
            or "access" in incident["title"].lower()
        ]

    elif signal_id == "business-transactions":
        filtered_incidents = [
            incident for incident in incidents
            if "transaction" in incident["title"].lower()
            or "business" in incident["category"].lower()
        ]

    else:
        filtered_incidents = incidents

    return {
        **incident_data,
        "incident_count": len(filtered_incidents),
        "open_incidents": len(filtered_incidents),
        "critical_incidents": len([i for i in filtered_incidents if i["severity"] == "CRITICAL"]),
        "high_incidents": len([i for i in filtered_incidents if i["severity"] == "HIGH"]),
        "incidents": filtered_incidents,
    }


def filter_anomaly_data(anomaly_data, signal_id):
    anomalies = anomaly_data.get("anomalies", [])

    if signal_id == "web-traffic":
        filtered_anomalies = [
            anomaly for anomaly in anomalies
            if anomaly["type"] in ["Traffic Spike", "Traffic Surge", "Error Burst", "Error Elevation"]
            or "http" in anomaly["source"].lower()
            or "www" in anomaly["source"].lower()
            or "access" in anomaly["source"].lower()
        ]

    elif signal_id == "security-access":
        filtered_anomalies = [
            anomaly for anomaly in anomalies
            if "auth" in anomaly["type"].lower()
            or "secure" in anomaly["source"].lower()
            or "access" in anomaly["source"].lower()
        ]

    elif signal_id == "business-transactions":
        filtered_anomalies = [
            anomaly for anomaly in anomalies
            if "vendor" in anomaly["source"].lower()
            or "sales" in anomaly["source"].lower()
            or "transaction" in anomaly["title"].lower()
        ]

    else:
        filtered_anomalies = anomalies

    return {
        **anomaly_data,
        "anomaly_count": len(filtered_anomalies),
        "critical_anomalies": len([a for a in filtered_anomalies if a["severity"] == "CRITICAL"]),
        "high_anomalies": len([a for a in filtered_anomalies if a["severity"] == "HIGH"]),
        "medium_anomalies": len([a for a in filtered_anomalies if a["severity"] == "MEDIUM"]),
        "anomalies": filtered_anomalies,
    }


@app.route("/")
def portfolio():
    agent = MonitoringAgent(ai_enabled=AI_ENABLED)
    data = agent.analyze()
    systems = build_systems(data)

    return render_template(
        "dashboard.html",
        systems=systems,
        data=data
    )


@app.route("/investigate")
def investigate_default():
    return investigate_signal("web-traffic")


@app.route("/investigate/<signal_id>")
def investigate_signal(signal_id):
    signal = get_signal(signal_id)

    monitoring_data = MonitoringAgent(ai_enabled=AI_ENABLED).analyze()
    data = filter_monitoring_data(monitoring_data, signal_id)

    incident_data = IncidentAgent(ai_enabled=AI_ENABLED).analyze()
    incident_data = filter_incident_data(incident_data, signal_id)

    anomaly_data = AnomalyAgent(ai_enabled=AI_ENABLED).analyze()
    anomaly_data = filter_anomaly_data(anomaly_data, signal_id)

    return render_template(
        "investigation.html",
        signal=signal,
        data=data,
        incident_data=incident_data,
        anomaly_data=anomaly_data
    )


@app.route("/status")
def status_default():
    return status_signal("web-traffic")


@app.route("/status/<signal_id>")
def status_signal(signal_id):
    signal = get_signal(signal_id)

    agent = MonitoringAgent(ai_enabled=AI_ENABLED)
    data = agent.analyze()
    data = filter_monitoring_data(data, signal_id)

    return render_template(
        "status.html",
        data=data,
        signal=signal
    )


@app.route("/incidents")
def incidents_default():
    return incidents_signal("web-traffic")


@app.route("/incidents/<signal_id>")
def incidents_signal(signal_id):
    signal = get_signal(signal_id)

    incident_agent = IncidentAgent(ai_enabled=AI_ENABLED)
    incident_data = incident_agent.analyze()
    incident_data = filter_incident_data(incident_data, signal_id)

    anomaly_agent = AnomalyAgent(ai_enabled=AI_ENABLED)
    anomaly_data = anomaly_agent.analyze()
    anomaly_data = filter_anomaly_data(anomaly_data, signal_id)

    rootcause_agent = RootCauseAgent(ai_enabled=AI_ENABLED)
    rootcause_data = rootcause_agent.analyze(
        signal=signal,
        incidents=incident_data["incidents"],
        anomalies=anomaly_data["anomalies"]
    )

    response_agent = ResponseAgent(ai_enabled=AI_ENABLED)
    response_data = response_agent.analyze(
        signal=signal,
        rootcause_data=rootcause_data,
        incidents=incident_data["incidents"],
        anomalies=anomaly_data["anomalies"]
    )

    return render_template(
        "incident_dashboard.html",
        incident_data=incident_data,
        rootcause_data=rootcause_data,
        response_data=response_data,
        signal=signal
    )


@app.route("/anomalies")
def anomalies_default():
    return anomalies_signal("web-traffic")


@app.route("/anomalies/<signal_id>")
def anomalies_signal(signal_id):
    signal = get_signal(signal_id)

    anomaly_agent = AnomalyAgent(ai_enabled=AI_ENABLED)
    anomaly_data = anomaly_agent.analyze()
    anomaly_data = filter_anomaly_data(anomaly_data, signal_id)

    incident_agent = IncidentAgent(ai_enabled=AI_ENABLED)
    incident_data = incident_agent.analyze()
    incident_data = filter_incident_data(incident_data, signal_id)

    rootcause_agent = RootCauseAgent(ai_enabled=AI_ENABLED)
    rootcause_data = rootcause_agent.analyze(
        signal=signal,
        incidents=incident_data["incidents"],
        anomalies=anomaly_data["anomalies"]
    )

    response_agent = ResponseAgent(ai_enabled=AI_ENABLED)
    response_data = response_agent.analyze(
        signal=signal,
        rootcause_data=rootcause_data,
        incidents=incident_data["incidents"],
        anomalies=anomaly_data["anomalies"]
    )

    return render_template(
        "anomaly_dashboard.html",
        anomaly_data=anomaly_data,
        rootcause_data=rootcause_data,
        response_data=response_data,
        signal=signal
    )


if __name__ == "__main__":
    app.run(debug=True)