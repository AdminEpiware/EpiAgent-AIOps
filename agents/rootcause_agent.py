from rules.rule_engine import RuleEngine
from ai.gemini_service import GeminiService, GeminiQuotaError, GeminiUnavailableError


class RootCauseAgent:

    def __init__(self, ai_enabled=False):
        self.rule_engine = RuleEngine()
        self.ai_enabled = ai_enabled
        self.gemini_service = GeminiService() if ai_enabled else None

    def analyze(self, signal, incidents=None, anomalies=None):
        incidents = incidents or []
        anomalies = anomalies or []

        total_events = self.rule_engine.get_total_events()
        total_server_errors = self.rule_engine.get_total_server_error_count()
        errors = self.rule_engine.get_error_summary()
        sources = self.rule_engine.get_top_sourcetypes()
        score = self.rule_engine.get_incident_score()
        health = self.rule_engine.get_system_health()

        root_causes = self.build_rule_based_root_causes(
            signal=signal,
            incidents=incidents,
            anomalies=anomalies,
            total_events=total_events,
            total_server_errors=total_server_errors,
            errors=errors,
            sources=sources,
            score=score,
            health=health
        )

        primary_root_cause = (
            root_causes[0]["title"]
            if root_causes
            else "No dominant root cause identified"
        )

        confidence = (
            root_causes[0]["confidence"]
            if root_causes
            else 60
        )

        ai_analysis = self.generate_ai_rootcause_summary(
            signal=signal,
            incidents=incidents,
            anomalies=anomalies,
            root_causes=root_causes,
            total_events=total_events,
            total_server_errors=total_server_errors,
            errors=errors,
            sources=sources,
            score=score,
            health=health
        )

        return {
            "root_cause_count": len(root_causes),
            "primary_root_cause": primary_root_cause,
            "confidence": confidence,
            "root_causes": root_causes,
            "ai_analysis": ai_analysis
        }

    def build_rule_based_root_causes(
        self,
        signal,
        incidents,
        anomalies,
        total_events,
        total_server_errors,
        errors,
        sources,
        score,
        health
    ):
        signal_id = signal.get("id", "")
        root_causes = []

        incident_titles = " ".join(
            incident.get("title", "") for incident in incidents
        ).lower()

        anomaly_types = " ".join(
            anomaly.get("type", "") for anomaly in anomalies
        ).lower()

        source_names = " ".join(
            source.get("sourcetype", "") for source in sources
        ).lower()

        if signal_id == "web-traffic":
            if total_server_errors > 0 or "500" in incident_titles or "503" in incident_titles:
                root_causes.append({
                    "id": "RCA-WEB-BACKEND",
                    "title": "Backend Service Instability",
                    "severity": "HIGH",
                    "confidence": 88,
                    "affected_area": signal.get("short_name", "Web Traffic"),
                    "evidence": (
                        f"{total_server_errors} server-side error events detected with "
                        f"{len(errors)} HTTP error pattern(s)."
                    ),
                    "reasoning": (
                        "HTTP 500/503 style incidents indicate backend service failure, "
                        "service timeout, or infrastructure availability degradation."
                    ),
                    "next_step": (
                        "Review backend service health, recent deployments, service logs, "
                        "and dependency availability."
                    )
                })

            if "traffic" in anomaly_types:
                root_causes.append({
                    "id": "RCA-WEB-TRAFFIC",
                    "title": "Traffic Concentration or Request Spike",
                    "severity": "MEDIUM",
                    "confidence": 82,
                    "affected_area": signal.get("short_name", "Web Traffic"),
                    "evidence": "Traffic spike or elevated source activity detected by Anomaly Agent.",
                    "reasoning": (
                        "High request concentration can overload application services and "
                        "increase HTTP 5xx errors."
                    ),
                    "next_step": (
                        "Check load balancer metrics, traffic source distribution, and autoscaling behavior."
                    )
                })

        elif signal_id == "security-access":
            if "auth" in anomaly_types or "secure" in source_names or "access" in source_names:
                root_causes.append({
                    "id": "RCA-SEC-AUTH",
                    "title": "Abnormal Authentication or Secure Access Activity",
                    "severity": "MEDIUM",
                    "confidence": 84,
                    "affected_area": signal.get("short_name", "Security Access"),
                    "evidence": "Secure access or authentication-related activity detected in Splunk signals.",
                    "reasoning": (
                        "Unexpected access volume can indicate login surge, authentication retry storms, "
                        "or access control misconfiguration."
                    ),
                    "next_step": (
                        "Review authentication logs, failed login patterns, access source IPs, and identity provider status."
                    )
                })

        elif signal_id == "business-transactions":
            if "vendor" in source_names or "sales" in source_names:
                root_causes.append({
                    "id": "RCA-BIZ-TXN",
                    "title": "Business Transaction Signal Deviation",
                    "severity": "LOW",
                    "confidence": 76,
                    "affected_area": signal.get("short_name", "Business Transactions"),
                    "evidence": "Business transaction source activity detected in Splunk operational signals.",
                    "reasoning": (
                        "Transaction activity changes can be caused by upstream vendor delays, "
                        "processing queue issues, or business workflow variation."
                    ),
                    "next_step": (
                        "Review transaction queues, vendor integration status, and recent business process changes."
                    )
                })

        if not root_causes and (incidents or anomalies):
            root_causes.append({
                "id": "RCA-GENERAL-OPS",
                "title": "Operational Signal Degradation",
                "severity": "MEDIUM",
                "confidence": 70,
                "affected_area": signal.get("short_name", "Operational Signal"),
                "evidence": (
                    f"{len(incidents)} incident(s) and {len(anomalies)} anomaly signal(s) detected."
                ),
                "reasoning": (
                    "The signal shows abnormal operational behavior, but available evidence is not enough "
                    "to isolate a single component-level root cause."
                ),
                "next_step": (
                    "Correlate Splunk source activity, error patterns, deployment history, and infrastructure metrics."
                )
            })

        if not root_causes:
            root_causes.append({
                "id": "RCA-NO-ISSUE",
                "title": "No Active Root Cause Identified",
                "severity": "LOW",
                "confidence": 65,
                "affected_area": signal.get("short_name", "Operational Signal"),
                "evidence": "No active incident or anomaly evidence found for this signal area.",
                "reasoning": (
                    "Current Splunk-derived evidence does not indicate a confirmed operational failure."
                ),
                "next_step": (
                    "Continue monitoring this signal area and re-run investigation if risk score increases."
                )
            })

        return root_causes

    def generate_ai_rootcause_summary(
        self,
        signal,
        incidents,
        anomalies,
        root_causes,
        total_events,
        total_server_errors,
        errors,
        sources,
        score,
        health
    ):
        if not self.ai_enabled:
            return (
                "AI analysis is disabled by configuration. "
                "Rule-based root cause analysis is active using live Splunk data."
            )

        try:
            prompt_data = {
                "signal": signal,
                "health": health,
                "score": score,
                "total_events": total_events,
                "total_server_errors": total_server_errors,
                "errors": errors,
                "sources": sources,
                "incidents": incidents,
                "anomalies": anomalies,
                "root_causes": root_causes
            }

            return self.gemini_service.generate_incident_analysis(prompt_data)

        except GeminiQuotaError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini API quota limit reached. "
                "Rule-based root cause analysis is active using live Splunk data."
            )

        except GeminiUnavailableError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini service is not reachable. "
                "Rule-based root cause analysis is active using live Splunk data."
            )

        except Exception:
            return (
                "AI analysis temporarily unavailable. "
                "Rule-based root cause analysis is active using live Splunk data."
            )