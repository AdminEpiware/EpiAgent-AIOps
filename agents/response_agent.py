from ai.gemini_service import GeminiService, GeminiQuotaError, GeminiUnavailableError


class ResponseAgent:

    def __init__(self, ai_enabled=False):
        self.ai_enabled = ai_enabled
        self.gemini_service = GeminiService() if ai_enabled else None

    def analyze(self, signal, rootcause_data=None, incidents=None, anomalies=None):
        rootcause_data = rootcause_data or {}
        incidents = incidents or []
        anomalies = anomalies or []

        recommended_actions = self.build_rule_based_actions(
            signal=signal,
            rootcause_data=rootcause_data,
            incidents=incidents,
            anomalies=anomalies
        )

        priority = self.calculate_priority(recommended_actions)

        ai_analysis = self.generate_ai_response_summary(
            signal=signal,
            rootcause_data=rootcause_data,
            incidents=incidents,
            anomalies=anomalies,
            recommended_actions=recommended_actions,
            priority=priority
        )

        return {
            "response_count": len(recommended_actions),
            "priority": priority,
            "recommended_actions": recommended_actions,
            "ai_analysis": ai_analysis
        }

    def build_rule_based_actions(self, signal, rootcause_data, incidents, anomalies):
        signal_id = signal.get("id", "")
        primary_root_cause = rootcause_data.get("primary_root_cause", "")
        actions = []

        if signal_id == "web-traffic":
            if "Backend Service Instability" in primary_root_cause:
                actions.extend([
                    {
                        "id": "ACT-WEB-001",
                        "title": "Validate backend service health",
                        "priority": "P1",
                        "owner": "Backend Engineering Team",
                        "action": "Check backend application logs, service status, error traces, and recent deployment changes.",
                        "expected_outcome": "Identify failing backend component responsible for HTTP 5xx errors."
                    },
                    {
                        "id": "ACT-WEB-002",
                        "title": "Scale affected application service",
                        "priority": "P1",
                        "owner": "Platform Operations Team",
                        "action": "Increase backend service capacity or validate autoscaling behavior if traffic pressure is high.",
                        "expected_outcome": "Reduce service saturation and lower HTTP 500/503 error rate."
                    },
                    {
                        "id": "ACT-WEB-003",
                        "title": "Check upstream dependency availability",
                        "priority": "P2",
                        "owner": "Infrastructure Team",
                        "action": "Review database, cache, gateway, and internal API dependency health.",
                        "expected_outcome": "Confirm whether backend failures are caused by dependency degradation."
                    }
                ])

            elif "Traffic" in primary_root_cause:
                actions.extend([
                    {
                        "id": "ACT-WEB-004",
                        "title": "Review traffic source concentration",
                        "priority": "P1",
                        "owner": "SRE / Observability Team",
                        "action": "Inspect high-volume sources, request paths, client IP patterns, and load balancer distribution.",
                        "expected_outcome": "Determine whether traffic spike is organic, bot-driven, or routing-related."
                    },
                    {
                        "id": "ACT-WEB-005",
                        "title": "Apply traffic protection controls",
                        "priority": "P2",
                        "owner": "Platform Operations Team",
                        "action": "Apply rate limits, caching, or routing adjustments if traffic is abnormal.",
                        "expected_outcome": "Stabilize web service response and prevent incident escalation."
                    }
                ])

        elif signal_id == "security-access":
            actions.extend([
                {
                    "id": "ACT-SEC-001",
                    "title": "Review authentication activity",
                    "priority": "P1",
                    "owner": "Security Operations Team",
                    "action": "Check authentication logs, failed login patterns, access source IPs, and identity provider health.",
                    "expected_outcome": "Identify whether access surge is normal user activity, retry storm, or suspicious behavior."
                },
                {
                    "id": "ACT-SEC-002",
                    "title": "Validate access control configuration",
                    "priority": "P2",
                    "owner": "Identity and Access Team",
                    "action": "Review recent IAM, SSO, firewall, and access policy changes.",
                    "expected_outcome": "Confirm that access behavior is not caused by misconfiguration."
                }
            ])

        elif signal_id == "business-transactions":
            actions.extend([
                {
                    "id": "ACT-BIZ-001",
                    "title": "Review transaction processing flow",
                    "priority": "P2",
                    "owner": "Business Operations Team",
                    "action": "Check vendor transaction queues, sales activity patterns, and processing delays.",
                    "expected_outcome": "Identify whether business workflow deviation is operational or expected."
                },
                {
                    "id": "ACT-BIZ-002",
                    "title": "Validate vendor integration status",
                    "priority": "P2",
                    "owner": "Integration Support Team",
                    "action": "Review vendor API availability, recent integration changes, and transaction failure logs.",
                    "expected_outcome": "Confirm whether vendor-side dependency is affecting transaction signals."
                }
            ])

        if not actions:
            actions.append({
                "id": "ACT-GEN-001",
                "title": "Continue investigation with correlated evidence",
                "priority": "P3",
                "owner": "Operations Team",
                "action": "Review Splunk source activity, incident evidence, anomaly patterns, and deployment history.",
                "expected_outcome": "Collect enough operational context to determine the correct remediation path."
            })

        return actions

    def calculate_priority(self, recommended_actions):
        priorities = [action.get("priority", "P3") for action in recommended_actions]

        if "P1" in priorities:
            return "HIGH"
        if "P2" in priorities:
            return "MEDIUM"
        return "LOW"

    def generate_ai_response_summary(
        self,
        signal,
        rootcause_data,
        incidents,
        anomalies,
        recommended_actions,
        priority
    ):
        if not self.ai_enabled:
            return (
                "AI analysis is disabled by configuration. "
                "Rule-based operational response recommendations are active using live Splunk-derived evidence."
            )

        try:
            prompt_data = {
                "signal": signal,
                "rootcause_data": rootcause_data,
                "incidents": incidents,
                "anomalies": anomalies,
                "recommended_actions": recommended_actions,
                "priority": priority
            }

            return self.gemini_service.generate_incident_analysis(prompt_data)

        except GeminiQuotaError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini API quota limit reached. "
                "Rule-based operational response recommendations are active using live Splunk-derived evidence."
            )

        except GeminiUnavailableError:
            return (
                "AI analysis temporarily unavailable. "
                "Gemini service is not reachable. "
                "Rule-based operational response recommendations are active using live Splunk-derived evidence."
            )

        except Exception:
            return (
                "AI analysis temporarily unavailable. "
                "Rule-based operational response recommendations are active using live Splunk-derived evidence."
            )