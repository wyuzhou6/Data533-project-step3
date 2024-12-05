# test_suite.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from test_medication import TestMedication
from test_prescription import TestPrescription
from test_inventory import TestInventory
from test_family import TestFamily
from test_reminder import TestReminder

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