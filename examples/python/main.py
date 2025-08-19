#!/usr/bin/env python3
"""
Main application entry point.
"""

from utils import helper_function
from data_processor import DataProcessor
# unused_module is imported but never used - should be detected as dead import

def main():
    """Main function."""
    print("Starting application...")
    helper_function("test")
    
    processor = DataProcessor()
    processor.process_data("sample.txt")
    
    print("Application completed.")

if __name__ == "__main__":
    main()