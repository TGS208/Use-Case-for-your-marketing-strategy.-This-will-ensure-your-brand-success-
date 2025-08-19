"""
This module is completely unused and should be detected as dead.
"""

def orphaned_function():
    """This function is in an orphaned file."""
    return "This file is never imported"

class OrphanedClass:
    """This class is in an orphaned file."""
    
    def __init__(self):
        self.value = 42
    
    def method(self):
        return self.value * 2