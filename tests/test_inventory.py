# test_inventory.py
# Unit tests for the InventoryManagement class.
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import shutil
from pathlib import Path
from medication_management.medication import Medication
from medication_management.inventory import InventoryManagement

class MockReminderSystem:
    """Mock reminder system to simulate reminders without an actual implementation."""
    def __init__(self):
        self.reminders = {}

    def set_reminder(self, member, med_id, message):
        """Set a reminder for a specific member and medication ID."""
        if member not in self.reminders:
            self.reminders[member] = {}
        self.reminders[member][med_id] = message
        print(f"Reminder set: {message}")

    def clear_reminder(self, member, med_id):
        """Clear a reminder for a specific member and medication ID."""
        if member in self.reminders and med_id in self.reminders[member]:
            del self.reminders[member][med_id]
            print(f"Cleared reminder for {member} - Medication ID {med_id}")

class TestInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up shared resources for all tests in the class."""
        print("\nSetting up TestInventory class...")
        cls.base_dir = Path("./test_data")
        cls.base_dir.mkdir(exist_ok=True)
        cls.data_dir = cls.base_dir / "data"
        cls.data_dir.mkdir(exist_ok=True)
        cls.reminder_system = MockReminderSystem()

    @classmethod
    def tearDownClass(cls):
        """Clean up shared resources after all tests in the class."""
        print("\nCleaning up TestInventory class...")
        try:
            if cls.base_dir.exists():
                shutil.rmtree(cls.base_dir)
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")

    def setUp(self):
        """Initialize resources for each test."""
        self.inventory = InventoryManagement(
            member_name="TestUser",
            base_dir=self.base_dir,
            reminder_system=self.reminder_system
        )
        self.test_med = Medication(
            name="Test Med",
            dosage="100mg",
            frequency="daily",
            daily_dosage=1,
            stock=10
        )

    def tearDown(self):
        """Clean up resources after each test."""
        self.inventory = None

    def test_add_medication(self):
        """Test adding medication to inventory"""
        med_id = self.inventory.add_medication(self.test_med)
        self.assertIn(med_id, self.inventory.medications)
        self.assertEqual(self.inventory.medications[med_id].name, "Test Med")
        self.assertEqual(self.inventory.medications[med_id].stock, 10)
        self.assertTrue(self.inventory.inventory_file.exists())

    def test_update_stock(self):
        """Test updating medication stock"""
        med_id = self.inventory.add_medication(self.test_med)
        self.assertTrue(self.inventory.update_stock(med_id, -5))
        self.assertEqual(self.inventory.medications[med_id].stock, 5)
        self.assertFalse(self.inventory.update_stock(med_id, -10))
        self.assertTrue(self.inventory.update_stock(med_id, 5))
        self.assertEqual(self.inventory.medications[med_id].stock, 10)

    def test_low_stock_check(self):
        """Test low stock detection"""
        # Create a medication with low stock (2.5 days supply)
        med1 = Medication(
            name="Low Med",
            dosage="100mg",
            frequency="daily",
            daily_dosage=2,
            stock=5
        )
        # Create a medication with sufficient stock
        med2 = Medication(
            name="OK Med",
            dosage="100mg",
            frequency="daily",
            daily_dosage=1,
            stock=10
        )
        
        med1_id = self.inventory.add_medication(med1)
        med2_id = self.inventory.add_medication(med2)
        
        low_stock = self.inventory.check_low_stock()
        # Verify only med1 is in low stock
        found_med = next((x for x in low_stock if x[0] == med1_id), None)
        self.assertIsNotNone(found_med)
        self.assertEqual(found_med[1], "Low Med")
        self.assertEqual(found_med[2], 2)  # 5/2 = 2 days supply
        
        # Verify med2 is not in low stock
        self.assertFalse(any(x[0] == med2_id for x in low_stock))

if __name__ == '__main__':
    unittest.main()