from config import SPLUNK_INDEX


TOTAL_EVENTS_QUERY = f"""
search index={SPLUNK_INDEX}
| stats count
"""

STATUS_QUERY = f"""
search index={SPLUNK_INDEX}
| stats count by status
"""

SOURCETYPE_QUERY = f"""
search index={SPLUNK_INDEX}
| stats count by sourcetype
"""

ERROR_QUERY = f"""
search index={SPLUNK_INDEX} status>=500
| stats count by status
"""

RECENT_ERROR_EVENTS_QUERY = f"""
search index={SPLUNK_INDEX} status>=500
| table _time host source sourcetype status uri_path method clientip
| head 20
"""
