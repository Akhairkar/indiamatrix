class BaseAdapter:
    """Base class for remote data adapters.

    run() returns True when local data changed, False when fetching succeeded
    but no update was needed, and None when the adapter failed. Keeping these
    states distinct prevents a failed fetch from looking like a clean run.
    """
    def __init__(self):
        self.name = "BaseAdapter"

    def fetch(self):
        """Fetch source data and return standardized data points."""
        raise NotImplementedError("Subclasses must implement fetch()")

    def update_local_data(self, fetched_data):
        """Update local records if newer or revised source values are found."""
        raise NotImplementedError("Subclasses must implement update_local_data()")

    def run(self):
        print(f"[{self.name}] Starting update check...")
        try:
            data = self.fetch()
            updated = self.update_local_data(data)
            print(f"[{self.name}] {'New data found and updated.' if updated else 'No new data found.'}")
            return bool(updated)
        except Exception as exc:
            print(f"[{self.name}] ERROR: {exc}")
            return None
