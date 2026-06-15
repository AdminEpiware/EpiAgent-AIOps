import time
import splunklib.client as client
import splunklib.results as results

from config import (
    SPLUNK_HOST,
    SPLUNK_PORT,
    SPLUNK_USERNAME,
    SPLUNK_PASSWORD,
)


class SplunkClient:
    """Small wrapper around Splunk SDK for EpiAgent AIOps."""

    def __init__(self):
        self.service = client.connect(
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            username=SPLUNK_USERNAME,
            password=SPLUNK_PASSWORD,
            scheme="https",
            verify=False,
        )

    def run_query(self, query, timeout_seconds=30):
        """Run an SPL query and return JSON result rows as a list of dicts."""
        job = self.service.jobs.create(query)

        start_time = time.time()
        while not job.is_done():
            if time.time() - start_time > timeout_seconds:
                job.cancel()
                raise TimeoutError(f"Splunk query timed out after {timeout_seconds} seconds")
            time.sleep(0.2)

        result_stream = job.results(output_mode="json")
        reader = results.JSONResultsReader(result_stream)

        data = []
        for item in reader:
            if isinstance(item, dict):
                data.append(item)

        return data
