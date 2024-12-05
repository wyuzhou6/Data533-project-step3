# test_prescription.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta
from medication_management.prescription import PrescriptionMedication

class TestPrescription(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nSetting up TestPrescription class...")
        cls.today = datetime.now().strftime("%Y-%m-%d")
        cls.tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        cls.yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    @classmethod
    def tearDownClass(cls):
        print("\nCleaning up TestPrescription class...")
        cls.today = None
        cls.tomorrow = None
        cls.yesterday = None

    def setUp(self):
        self.prescription = PrescriptionMedication(
            name="Test Prescription",
            dosage="250mg",
            frequency="twice daily",
            daily_dosage=2,
            stock=14,
            doctor_name="Dr. Test",
            prescription_date=self.today,
            indication="Test condition",
            warnings="Test warning",
            expiration_date=self.tomorrow
        )

    def tearDown(self):
        self.prescription = None

    def test_prescription_initialization(self):
        """Test prescription object creation and attributes"""
        self.assertEqual(self.prescription.name, "Test Prescription")
        self.assertEqual(self.prescription.doctor_name, "Dr. Test")
        self.assertEqual(self.prescription.prescription_date, self.today)
        self.assertEqual(self.prescription.expiration_date, self.tomorrow)
        self.assertEqual(self.prescription.indication, "Test condition")

    def test_expiration_check(self):
        """Test expiration date validation"""
        self.assertFalse(self.prescription.is_expired())
        
        expired_prescription = PrescriptionMedication(
            name="Expired Med",
            dosage="250mg",
            frequency="twice daily",
            daily_dosage=2,
            stock=14,
            doctor_name="Dr. Test",
            prescription_date=self.yesterday,
            indication="Test",
            warnings="Test",
            expiration_date=self.yesterday
        )
        self.assertTrue(expired_prescription.is_expired())

    def test_invalid_dates(self):
        """Test invalid date handling"""
        with self.assertRaises(ValueError):
            PrescriptionMedication(
                name="Invalid Date Med",
                dosage="250mg",
                frequency="twice daily",
                daily_dosage=2,
                stock=14,
                doctor_name="Dr. Test",
                prescription_date="invalid-date",
                indication="Test",
                warnings="Test",
                expiration_date=self.tomorrow
            )
        
        with self.assertRaises(ValueError):
            PrescriptionMedication(
                name="Invalid Date Med",
                dosage="250mg",
                frequency="twice daily",
                daily_dosage=2,
                stock=14,
                doctor_name="Dr. Test",
                prescription_date=self.today,
                indication="Test",
                warnings="Test",
                expiration_date="invalid-date"
            )

if __name__ == '__main__':
    unittest.main()