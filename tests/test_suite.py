# test_suite.py
# A script to aggregate and run all unit tests for the project
import sys
import os
# Test Travis
# Add the project's root directory to the Python module search path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
# Import all test classes to include in the test suite.
from tests.test_medication import TestMedication
from tests.test_prescription import TestPrescription
from tests.test_inventory import TestInventory
from tests.test_family import TestFamily
from tests.test_reminder import TestReminder

def create_test_suite():
    """Create and return a test suite containing all test cases"""
    suite = unittest.TestSuite()
    
    # Add all test cases from each test class
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMedication))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPrescription))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInventory))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFamily))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestReminder))
    
    return suite

if __name__ == '__main__':
    # Create and run the test suite
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate status code
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)