# test_reminder.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import shutil
from pathlib import Path
from user_management.reminder import ReminderSystem

class TestReminder(unittest.TestCase):
    """
    A test suite for the ReminderSystem module.

    This class verifies the key functionalities of the ReminderSystem, including:
    - Adding, retrieving, and updating reminders.
    - Clearing specific or all reminders.
    - Handling low stock alerts.
    - Ensuring data persistence across instances.
    """

    @classmethod
    def setUpClass(cls):
        """
        Class-level setup method.
        Initializes the base and data directories for storing reminder data.
        Called once before any test methods are executed.
        """
        print("\nSetting up TestReminder class...")
        cls.base_dir = Path("./test_data")  # Path to the base directory for testing
        cls.base_dir.mkdir(exist_ok=True)  # Create the base directory if it doesn't exist
        cls.data_dir = cls.base_dir / "data"  # Path to the data directory
        cls.data_dir.mkdir(exist_ok=True)  # Create the data directory

    @classmethod
    def tearDownClass(cls):
        """
        Class-level teardown method.
        Cleans up test directories and files after all test methods are executed.
        """
        print("\nCleaning up TestReminder class...")
        try:
            if cls.base_dir.exists():
                shutil.rmtree(cls.base_dir)  # Remove the test directories
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")  # Log any cleanup errors

    def setUp(self):
        """
        Test-level setup method.
        Initializes a new ReminderSystem instance and adds some sample reminders.
        Called before each test method.
        """
        self.reminder_system = ReminderSystem(self.base_dir)  # Initialize ReminderSystem
        # Add initial reminders for testing
        self.reminder_system.set_reminder("TestUser", 1, "Test reminder 1")
        self.reminder_system.set_reminder("TestUser", 2, "Test reminder 2")

    def tearDown(self):
        """
        Test-level teardown method.
        Cleans up the ReminderSystem instance.
        Called after each test method.
        """
        self.reminder_system = None  # Dereference the ReminderSystem instance

    def test_set_and_get_reminder(self):
        """
        Test case for setting and retrieving reminders.
        
        Verifies:
        - Reminders can be added for a user.
        - Reminders can be retrieved correctly.
        - Existing reminders can be updated.
        """
        self.reminder_system.set_reminder("TestUser", 3, "Test reminder 3")  # Add a new reminder
        self.assertIn("TestUser", self.reminder_system.reminders)  # Ensure user exists
        self.assertIn(3, self.reminder_system.reminders["TestUser"])  # Ensure reminder exists
        self.assertEqual(
            self.reminder_system.reminders["TestUser"][3],
            "Test reminder 3"
        )  # Verify reminder content

        # Update an existing reminder
        self.reminder_system.set_reminder("TestUser", 3, "Updated reminder")
        self.assertEqual(
            self.reminder_system.reminders["TestUser"][3],
            "Updated reminder"
        )  # Verify updated content

    def test_clear_reminder(self):
        """
        Test case for clearing specific reminders.
        
        Verifies:
        - Specific reminders can be cleared successfully.
        - Attempting to clear non-existent reminders does not cause errors.
        """
        self.reminder_system.clear_reminder("TestUser", 1)  # Clear an existing reminder
        self.assertNotIn(1, self.reminder_system.reminders["TestUser"])  # Verify reminder is cleared
        self.assertIn(2, self.reminder_system.reminders["TestUser"])  # Ensure other reminders remain
        
        # Attempt to clear non-existent reminders
        self.reminder_system.clear_reminder("TestUser", 999)  # Reminder ID does not exist
        self.reminder_system.clear_reminder("NonexistentUser", 1)  # User does not exist

    def test_check_alerts(self):
        """
        Test case for handling low stock alerts.
        
        Verifies:
        - Alerts for low stock items are added as reminders.
        - The content of the alerts is correctly formatted.
        """
        low_stock_warnings = [
            (4, "Med1", 2),  # Alert 1: Medicine "Med1" with low stock of 2
            (5, "Med2", 1)   # Alert 2: Medicine "Med2" with low stock of 1
        ]
        self.reminder_system.check_alerts("TestUser", low_stock_warnings)  # Add alerts
        
        # Verify alerts are added as reminders
        self.assertIn(4, self.reminder_system.reminders["TestUser"])
        self.assertIn(5, self.reminder_system.reminders["TestUser"])
        self.assertIn("Med1", self.reminder_system.reminders["TestUser"][4])  # Verify content of alert 1
        self.assertIn("Med2", self.reminder_system.reminders["TestUser"][5])  # Verify content of alert 2

    def test_clear_all_reminders(self):
        """
        Test case for clearing all reminders for a user.
        
        Verifies:
        - All reminders for a specific user can be cleared.
        - Clearing reminders for a non-existent user does not cause errors.
        """
        self.reminder_system.clear_all_reminders("TestUser")  # Clear all reminders
        self.assertEqual(len(self.reminder_system.reminders["TestUser"]), 0)  # Verify all reminders are cleared
        
        # Attempt to clear reminders for a non-existent user
        self.reminder_system.clear_all_reminders("NonexistentUser")  # User does not exist

    def test_persistence(self):
        """
        Test case for ensuring reminder data persistence.
        
        Verifies:
        - Reminders are saved to the file system.
        - Reminders are correctly loaded when a new ReminderSystem instance is created.
        """
        # Create a new instance of ReminderSystem to load saved data
        new_reminder_system = ReminderSystem(self.base_dir)
        
        # Verify loaded data matches the saved data
        self.assertIn("TestUser", new_reminder_system.reminders)  # Ensure user exists
        self.assertIn(1, new_reminder_system.reminders["TestUser"])  # Verify reminder 1 exists
        self.assertIn(2, new_reminder_system.reminders["TestUser"])  # Verify reminder 2 exists
        self.assertEqual(
            new_reminder_system.reminders["TestUser"][1],
            "Test reminder 1"
        )  # Verify content of reminder 1

if __name__ == '__main__':
    unittest.main()
