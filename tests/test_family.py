# test_family.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import shutil
from pathlib import Path
from user_management.family import FamilyManagement
from user_management.reminder import ReminderSystem

class TestFamily(unittest.TestCase):
    """
    A test suite for the FamilyManagement system.

    This class tests key functionalities of the FamilyManagement module, including:
    - Adding new family members.
    - Switching between members.
    - Deleting members.
    
    It uses unittest's setup and teardown mechanisms to ensure tests are isolated and
    the environment is cleaned up after execution.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup method.
        Initializes test directories and the ReminderSystem instance.
        Called once before any test methods are executed.
        """
        print("\nSetting up TestFamily class...")
        cls.base_dir = Path("./test_data")  # Path to test data directory
        cls.base_dir.mkdir(exist_ok=True)  # Create test data directory if it doesn't exist
        cls.data_dir = cls.base_dir / "data"  # Subdirectory for test data
        cls.data_dir.mkdir(exist_ok=True)  # Create data directory
        cls.reminder_system = ReminderSystem(cls.base_dir)  # Initialize the reminder system
    
    @classmethod
    def tearDownClass(cls):
        """
        Class-level teardown method.
        Cleans up test directories and files created during testing.
        Called once after all test methods are executed.
        """
        print("\nCleaning up TestFamily class...")
        try:
            if cls.base_dir.exists():
                shutil.rmtree(cls.base_dir)  # Remove the base directory and its contents
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")  # Log any cleanup errors

    def setUp(self):
        """
        Test-level setup method.
        Initializes a new FamilyManagement instance and ensures the member list is empty.
        Called before every test method.
        """
        self.family_manager = FamilyManagement(
            self.base_dir,  # Directory for storing family data
            self.reminder_system  # Associated reminder system
        )
        # Clear all existing members
        for member in list(self.family_manager.members.keys()):
            self.family_manager.delete_member(member)

    def tearDown(self):
        """
        Test-level teardown method.
        Cleans up the FamilyManagement instance.
        Called after every test method.
        """
        self.family_manager = None  # Dereference the FamilyManagement instance

    def test_add_member(self):
        """
        Test case for adding family members.
        
        Verifies:
        - New members can be added successfully.
        - Members appear in the member list after being added.
        - Duplicate members cannot be added.
        """
        # Ensure the test members do not already exist
        if "John" in self.family_manager.members:
            self.family_manager.delete_member("John")
        if "Jane" in self.family_manager.members:
            self.family_manager.delete_member("Jane")
        
        # Add members and verify they were added
        self.assertTrue(self.family_manager.add_member("John"))
        self.assertTrue(self.family_manager.add_member("Jane"))
        self.assertIn("John", self.family_manager.members)
        self.assertIn("Jane", self.family_manager.members)
        # Verify duplicate members cannot be added
        self.assertFalse(self.family_manager.add_member("John"))

    def test_member_switching(self):
        """
        Test case for switching between family members.
        
        Verifies:
        - Members can be switched to successfully.
        - The current member updates correctly.
        - Non-existent members cannot be switched to.
        """
        # Ensure the test members do not already exist
        if "John" in self.family_manager.members:
            self.family_manager.delete_member("John")
        if "Jane" in self.family_manager.members:
            self.family_manager.delete_member("Jane")
        
        # Add members
        self.family_manager.add_member("John")
        self.family_manager.add_member("Jane")
        
        # Test switching between members
        self.assertTrue(self.family_manager.switch_member("John"))
        self.assertEqual(self.family_manager.current_member, "John")
        self.assertTrue(self.family_manager.switch_member("Jane"))
        self.assertEqual(self.family_manager.current_member, "Jane")
        # Verify non-existent members cannot be switched to
        self.assertFalse(self.family_manager.switch_member("NonExistent"))

    def test_member_deletion(self):
        """
        Test case for deleting family members.
        
        Verifies:
        - Existing members can be deleted successfully.
        - Deleted members no longer appear in the member list.
        - Non-existent members cannot be deleted.
        """
        # Add a member for testing
        self.family_manager.add_member("John")
        
        # Test deleting an existing member
        self.assertTrue(self.family_manager.delete_member("John"))
        self.assertNotIn("John", self.family_manager.members)
        
        # Verify non-existent members cannot be deleted
        self.assertFalse(self.family_manager.delete_member("NonExistent"))

if __name__ == '__main__':
    unittest.main()
