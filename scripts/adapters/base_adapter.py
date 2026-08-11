class BaseAdapter:
    """
    Base class for all data adapters.
    Each adapter is responsible for fetching data from a specific source
    and updating the local JSON files if new data is found.
    """
    
    def __init__(self):
        self.name = "BaseAdapter"
        
    def fetch(self):
        """
        Fetch data from the remote source.
        Returns a dictionary or list of standardized data points.
        """
        raise NotImplementedError("Subclasses must implement fetch()")
        
    def update_local_data(self, fetched_data):
        """
        Compare fetched data with local JSON files.
        If new data is found, update the local JSON and return True.
        Otherwise, return False.
        """
        raise NotImplementedError("Subclasses must implement update_local_data()")
        
    def run(self):
        """
        Execute the adapter pipeline.
        """
        print(f"[{self.name}] Starting update check...")
        try:
            data = self.fetch()
            updated = self.update_local_data(data)
            if updated:
                print(f"[{self.name}] New data found and updated.")
            else:
                print(f"[{self.name}] No new data found.")
            return updated
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            return False
