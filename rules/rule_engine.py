import time

try:
    from splunk.splunk_client import SplunkClient
    from splunk.spl_queries import (
        TOTAL_EVENTS_QUERY,
        ERROR_QUERY,
        SOURCETYPE_QUERY,
    )
except Exception:
    SplunkClient = None
    TOTAL_EVENTS_QUERY = None
    ERROR_QUERY = None
    SOURCETYPE_QUERY = None


class RuleEngine:
    """
    Rule engine using live Splunk data.

    Splunk is always the source of truth.
    AI_ENABLED only controls Gemini usage.

    Cache is used to avoid running the same Splunk queries repeatedly
    during dashboard navigation.
    """

    _splunk_client = None
    _splunk_available = False
    _splunk_error = None

    _cache = {}
    _cache_ttl_seconds = 60

    def __init__(self):
        self.splunk_client = self._get_splunk_client()
        self.splunk_available = RuleEngine._splunk_available
        self.splunk_error = RuleEngine._splunk_error

    @classmethod
    def _get_splunk_client(cls):
        if cls._splunk_client:
            return cls._splunk_client

        if not SplunkClient:
            cls._splunk_error = "SplunkClient import failed"
            cls._splunk_available = False
            return None

        try:
            cls._splunk_client = SplunkClient()
            cls._splunk_available = True
            cls._splunk_error = None
            return cls._splunk_client

        except Exception as exc:
            cls._splunk_error = str(exc)
            cls._splunk_available = False
            print(f"[RuleEngine] Splunk connection failed: {exc}")
            return None

    @classmethod
    def _get_cached_result(cls, query):
        cached = cls._cache.get(query)

        if not cached:
            return None

        cached_time = cached.get("time", 0)
        age = time.time() - cached_time

        if age <= cls._cache_ttl_seconds:
            return cached.get("data", [])

        return None

    @classmethod
    def _set_cached_result(cls, query, data):
        cls._cache[query] = {
            "time": time.time(),
            "data": data
        }

    def _run_splunk_query(self, query):
        if not self.splunk_client or not query:
            return []

        cached_data = self._get_cached_result(query)

        if cached_data is not None:
            return cached_data

        try:
            data = self.splunk_client.run_query(query)
            self._set_cached_result(query, data)
            return data

        except Exception as exc:
            RuleEngine._splunk_error = str(exc)
            self.splunk_error = str(exc)
            print(f"[RuleEngine] Splunk query failed: {exc}")
            return []

    def get_total_events(self):
        rows = self._run_splunk_query(TOTAL_EVENTS_QUERY)

        if rows:
            return int(rows[0].get("count", 0))

        return 0

    def get_total_server_error_count(self):
        rows = self._run_splunk_query(ERROR_QUERY)

        if rows:
            return sum(int(row.get("count", 0)) for row in rows)

        return 0

    def get_detected_server_error_types(self):
        rows = self._run_splunk_query(ERROR_QUERY)

        if rows:
            return len(rows)

        return 0

    def get_system_health(self):
        total_errors = self.get_total_server_error_count()

        if total_errors > 5000:
            return "RED"
        elif total_errors > 1000:
            return "WARNING"
        else:
            return "GREEN"

    def get_error_summary(self):
        rows = self._run_splunk_query(ERROR_QUERY)

        if rows:
            return [
                f"HTTP {row.get('status', 'unknown')} : {row.get('count', 0)} events"
                for row in rows
            ]

        return []

    def get_top_sourcetypes(self):
        rows = self._run_splunk_query(SOURCETYPE_QUERY)

        if rows:
            return sorted(
                rows,
                key=lambda item: int(item.get("count", 0)),
                reverse=True
            )

        return []

    def get_incident_score(self):
        total_errors = self.get_total_server_error_count()

        if total_errors > 5000:
            return 95
        elif total_errors > 1000:
            return 70
        elif total_errors > 500:
            return 50
        else:
            return 20

    def generate_recommendation(self):
        score = self.get_incident_score()

        if score >= 90:
            return "Critical server-side instability detected from live Splunk signals. Immediate investigation is required."
        elif score >= 70:
            return "High number of server-side errors detected from live Splunk signals. Review failing services and backend logs."
        elif score >= 50:
            return "Moderate operational risk detected from live Splunk signals. Continue monitoring affected services."
        else:
            return "Live Splunk signals indicate the system is operating normally."