from rules.rule_engine import RuleEngine
from ai.gemini_service import GeminiService, GeminiQuotaError, GeminiUnavailableError


class AnomalyAgent:

    def __init__(self, ai_enabled=False):
        self.rule_engine = RuleEngine()
        self.ai_enabled = ai_enabled
        self.gemini_service = GeminiService() if ai_enabled else None

    def analyze(self):
        total_events = self.rule_engine.get_total_events()
        total_server_errors = self.rule_engine.get_total_server_error_count()
        errors = self.rule_engine.get_error_summary()
        sources = self.rule_engine.get_top_sourcetypes()
        score = self.rule_engine.get_incident_score()
        health = self.rule_engine.get_system_health()

        anomalies = []

        for source in sources:
            source_name = source.get("sourcetype", "Unknown Source")
            count = int(source.get("count", 0))

            contribution = round((count / total_events) * 100, 2) if total_events > 0 else 0

            if contribution >= 35:
                anomalies.append({
                    "id": "ANOM-TRAFFIC-SPIKE",
                    "type": "Traffic Spike",
                    "title": "High Traffic Concentration Detected",
                    "severity": "CRITICAL",
                    "source": source_name,
                    "confidence": 94,
                    "evidence": f"{source_name} generated {count} events, contributing {contribution}% of total Splunk signals.",
                    "owner": "SRE / Observability Team"
                })

            elif contribution >= 25:
                anomalies.append({
                    "id": "ANOM-TRAFFIC-SURGE",
                    "type": "Traffic Surge",
                    "title": "Elevated Source Activity Detected",
                    "severity": "HIGH",
                    "source": source_name,
                    "confidence": 88,
                    "evidence": f"{source_name} generated {count} events, contributing {contribution}% of total Splunk signals.",
                    "owner": "Platform Operations Team"
                })

        if total_server_errors >= 2000:
            anomalies.append({
                "id": "ANOM-ERROR-BURST",
                "type": "Error Burst",
                "title": "Server Error Burst Detected",
                "severity": "HIGH",
                "source": "HTTP 5xx status signals",
                "confidence": 91,
                "evidence": f"{total_server_errors} server-side error events detected across {len(errors)} error patterns.",
                "owner": "Backend Engineering Team"
            })

        elif total_server_errors >= 1000:
            anomalies.append({
                "id": "ANOM-ERROR-ELEVATION",
                "type": "Error Elevation",
                "title": "Elevated Server Error Activity Detected",
                "severity": "MEDIUM",
                "source": "HTTP 5xx status signals",
                "confidence": 82,
                "evidence": f"{total_server_errors} server-side error events detected across {len(errors)} error patterns.",
                "owner": "Application Support Team"
            })

        for source in sources:
            source_name = source.get("sourcetype", "Security Source")
            count = int(source.get("count", 0))

            if "secure" in source_name.lower() and count >= 30000:
                anomalies.append({
                    "id": "ANOM-AUTH-SURGE",
                    "type": "Authentication Surge",
                    "title": "Secure Access Activity Surge Detected",
                    "severity": "MEDIUM",
                    "source": source_name,
                    "confidence": 86,
                    "evidence": f"{source_name} generated {count} secure access events.",
                    "owner": "Security Operations Team"
                })

        ai_analysis = self.generate_ai_summary(
            anomalies=anomalies,
            health=health,
            score=score,
            total_events=total_events,
            total_server_errors=total_server_errors,
            sources=sources
        )

        return {
            "anomaly_count": len(anomalies),
            "critical_anomalies": len([a for a in anomalies if a["severity"] == "CRITICAL"]),
            "high_anomalies": len([a for a in anomalies if a["severity"] == "HIGH"]),
            "medium_anomalies": len([a for a in anomalies if a["severity"] == "MEDIUM"]),
            "anomalies": anomalies,
            "ai_analysis": ai_analysis
        }

    def get_sample_data(self):
        return self.analyze()

    def generate_ai_summary(
        self,
        anomalies,
        health,
        score,
        total_events,
        total_server_errors,
        sources
    ):
        if not self.ai_enabled:
            return (
                "AI analysis is disabled by configuration. "
                "Rule-based anomaly analysis is active using live Splunk data."
            )

        prompt_data = {
            "health": health,
            "score": score,
            "total_events": total_events,
            "total_server_errors": total_server_errors,
            "anomalies": anomalies,
            "sources": sources
        }

        try:
            return self.gemini_service.generate_incident_analysis(prompt_data)

        except GeminiQuotaError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini API quota limit reached. "
                "Rule-based anomaly analysis is active using live Splunk data."
            )

        except GeminiUnavailableError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini service is not reachable. "
                "Rule-based anomaly analysis is active using live Splunk data."
            )

        except Exception:
            return (
                "AI analysis temporarily unavailable. "
                "Rule-based anomaly analysis is active using live Splunk data."
            )