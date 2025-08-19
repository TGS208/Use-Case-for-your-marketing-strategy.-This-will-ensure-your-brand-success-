"""
Data processing module.
"""

class DataProcessor:
    """Handles data processing operations."""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_data(self, filename):
        """Process data from a file."""
        print(f"Processing data from {filename}")
        self.processed_count += 1
        return True
    
    def unused_method(self):
        """This method is never called - dead code."""
        return "Unused method"