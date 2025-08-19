#!/usr/bin/env python3
"""
Example usage script for the Dead Code Detector.
Demonstrates how to use the tool programmatically.
"""

import os
import sys
from dead_code_detector import DeadCodeDetector

def main():
    """Example usage of the Dead Code Detector."""
    print("Dead Code Detector - Example Usage")
    print("=" * 40)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(current_dir, 'examples')
    
    if not os.path.exists(examples_dir):
        print(f"Examples directory not found: {examples_dir}")
        return 1
    
    # Initialize detector with config
    config_file = os.path.join(current_dir, 'dead_code_config.json')
    detector = DeadCodeDetector(config_file if os.path.exists(config_file) else None)
    
    # Analyze examples directory
    print(f"Analyzing: {examples_dir}")
    detector.scan_directory(examples_dir)
    
    # Generate and display report
    report = detector.generate_report()
    print(report)
    
    # Show additional details
    print("\nAdditional Analysis:")
    print("-" * 20)
    print(f"Files analyzed: {len(detector.all_files)}")
    print(f"Dependencies found: {len(detector.file_dependencies)}")
    
    # Show file dependencies
    if detector.file_dependencies:
        print("\nFile Dependencies:")
        for file_path, deps in detector.file_dependencies.items():
            if deps:
                short_file = os.path.basename(file_path)
                dep_names = [os.path.basename(dep) for dep in deps]
                print(f"  {short_file} -> {', '.join(dep_names)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())