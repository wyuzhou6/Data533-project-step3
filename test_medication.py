# test_medication.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from medication_management.medication import Medication

class TestMedication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """One-time setup for the entire class"""
        print("\nSetting up TestMedication class...")
        cls.default_daily_dosage = 2
        cls.default_stock = 20

    @classmethod
    def tearDownClass(cls):
        """One-time cleanup for the entire class"""
        print("\nCleaning up TestMedication class...")
        cls.default_daily_dosage = None
        cls.default_stock = None

    def setUp(self):
        """Setup before each test"""
        self.med = Medication(
            name="Test Med",
            dosage="100mg",
            frequency="twice daily",
            daily_dosage=self.default_daily_dosage,
            stock=self.default_stock
        )

    def tearDown(self):
        """Cleanup after each test"""
        self.med = None

    def test_medication_initialization(self):
        """Test medication object creation and attributes"""
        self.assertEqual(self.med.name, "Test Med")
        self.assertEqual(self.med.dosage, "100mg")
        self.assertEqual(self.med.frequency, "twice daily")
        self.assertEqual(self.med.daily_dosage, 2)
        self.assertEqual(self.med.stock, 20)

    def test_calculate_days_left(self):
        """Test days left calculation"""
        self.assertEqual(self.med.calculate_days_left(), 10)  # 20/2 = 10 days
        self.med.stock = 15
        self.assertEqual(self.med.calculate_days_left(), 7)   # 15/2 = 7.5 -> 7 days
        with self.assertRaises(ValueError):
            self.med.daily_dosage = 0
            self.med.calculate_days_left()
        with self.assertRaises(ValueError):
            self.med.daily_dosage = -1
            self.med.calculate_days_left()

    def test_update_stock(self):
        """Test stock update functionality"""
        self.assertTrue(self.med.update_stock(-5))
        self.assertEqual(self.med.stock, 15)
        self.assertTrue(self.med.update_stock(5))
        self.assertEqual(self.med.stock, 20)
        self.assertFalse(self.med.update_stock(-25))
        self.assertEqual(self.med.stock, 20)

if __name__ == '__main__':
    unittest.main()