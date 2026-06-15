from rules.rule_engine import RuleEngine
from ai.gemini_service import GeminiService, GeminiQuotaError, GeminiUnavailableError


class MonitoringAgent:

    def __init__(self, ai_enabled=False):
        self.rule_engine = RuleEngine()
        self.ai_enabled = ai_enabled
        self.gemini_service = GeminiService() if ai_enabled else None

    def analyze(self):
        result = {
            "total_events": self.rule_engine.get_total_events(),
            "server_error_count": self.rule_engine.get_detected_server_error_types(),
            "total_server_errors": self.rule_engine.get_total_server_error_count(),
            "health": self.rule_engine.get_system_health(),
            "score": self.rule_engine.get_incident_score(),
            "recommendation": self.rule_engine.generate_recommendation(),
            "errors": self.rule_engine.get_error_summary(),
            "sources": self.rule_engine.get_top_sourcetypes(),
            "splunk_available": self.rule_engine.splunk_available,
            "splunk_error": self.rule_engine.splunk_error,
        }

        result["ai_summary"] = self.generate_ai_summary(result)

        return result

    def generate_ai_summary(self, result):
        if not self.ai_enabled:
            return (
                "AI analysis is disabled by configuration. "
                "Rule-based monitoring analysis is active using live Splunk data."
            )

        try:
            return self.gemini_service.generate_incident_analysis(result)

        except GeminiQuotaError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini API quota limit reached. "
                "Rule-based monitoring analysis is active using live Splunk data. "
                f"{result['recommendation']}"
            )

        except GeminiUnavailableError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini service is not reachable. "
                "Rule-based monitoring analysis is active using live Splunk data. "
                f"{result['recommendation']}"
            )

        except Exception:
            return (
                "AI analysis temporarily unavailable. "
                "Rule-based monitoring analysis is active using live Splunk data. "
                f"{result['recommendation']}"
            )