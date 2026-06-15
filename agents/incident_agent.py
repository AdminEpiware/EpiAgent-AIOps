from rules.rule_engine import RuleEngine
from ai.gemini_service import GeminiService, GeminiQuotaError, GeminiUnavailableError


class IncidentAgent:

    def __init__(self, ai_enabled=False):
        self.rule_engine = RuleEngine()
        self.ai_enabled = ai_enabled
        self.gemini_service = GeminiService() if ai_enabled else None

    def analyze(self):
        errors = self.rule_engine.get_error_summary()
        score = self.rule_engine.get_incident_score()
        health = self.rule_engine.get_system_health()
        sources = self.rule_engine.get_top_sourcetypes()

        incidents = []

        for error in errors:
            if "503" in error:
                incidents.append({
                    "id": "INC-503",
                    "title": "Service Unavailable Errors Detected",
                    "severity": "HIGH",
                    "status": "OPEN",
                    "category": "Availability",
                    "evidence": error,
                    "owner": "Infrastructure Team"
                })

            elif "500" in error:
                incidents.append({
                    "id": "INC-500",
                    "title": "Internal Server Errors Detected",
                    "severity": "HIGH",
                    "status": "OPEN",
                    "category": "Application",
                    "evidence": error,
                    "owner": "Backend Engineering Team"
                })

            elif "505" in error:
                incidents.append({
                    "id": "INC-505",
                    "title": "HTTP Version Compatibility Issue",
                    "severity": "MEDIUM",
                    "status": "OPEN",
                    "category": "Protocol",
                    "evidence": error,
                    "owner": "Platform Team"
                })

        ai_analysis = self.generate_ai_incident_report(
            incidents=incidents,
            health=health,
            score=score,
            sources=sources
        )

        return {
            "incident_count": len(incidents),
            "open_incidents": len(incidents),
            "critical_incidents": len([i for i in incidents if i["severity"] == "CRITICAL"]),
            "high_incidents": len([i for i in incidents if i["severity"] == "HIGH"]),
            "incidents": incidents,
            "ai_analysis": ai_analysis
        }

    def generate_ai_incident_report(self, incidents, health, score, sources):
        if not self.ai_enabled:
            return (
                "AI analysis is disabled by configuration. "
                "Rule-based incident analysis is active using live Splunk data."
            )

        prompt_data = {
            "health": health,
            "score": score,
            "incidents": incidents,
            "sources": sources
        }

        try:
            return self.gemini_service.generate_incident_analysis(prompt_data)

        except GeminiQuotaError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini API quota limit reached. "
                "Rule-based incident analysis is active using live Splunk data."
            )

        except GeminiUnavailableError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini service is not reachable. "
                "Rule-based incident analysis is active using live Splunk data."
            )

        except Exception:
            return (
                "AI analysis temporarily unavailable. "
                "Rule-based incident analysis is active using live Splunk data."
            )