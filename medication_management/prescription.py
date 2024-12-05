# prescription.py
from datetime import datetime
from medication_management.medication import Medication

class PrescriptionMedication(Medication):
    """
    A class representing a prescription medication, inheriting from Medication.

    Attributes:
        doctor_name (str): The name of the prescribing doctor.
        prescription_date (str): The date the prescription was issued (YYYY-MM-DD).
        indication (str): The medical indication for the medication.
        warnings (str): Any warnings associated with the medication.
        expiration_date (str): The expiration date of the medication (YYYY-MM-DD).
    """
    def __init__(self, name, dosage, frequency, daily_dosage, stock, doctor_name, prescription_date, indication, warnings, expiration_date):
        """
        Initialize a PrescriptionMedication object.

        Args:
            name (str): The name of the medication.
            dosage (str): The dosage information (e.g., "500mg").
            frequency (str): The frequency of intake (e.g., "2 times/day").
            daily_dosage (int): The daily dosage (number of units per day).
            stock (int): The current stock level.
            doctor_name (str): The name of the prescribing doctor.
            prescription_date (str): The date the prescription was issued (YYYY-MM-DD).
            indication (str): The medical indication for the medication.
            warnings (str): Any warnings associated with the medication.
            expiration_date (str): The expiration date of the medication (YYYY-MM-DD).

        Raises:
            ValueError: If the dates are not in the correct format (YYYY-MM-DD).
        """
        # Initialize attributes inherited from the Medication class
        super().__init__(name, dosage, frequency, daily_dosage, stock)
        # Set additional attributes specific to prescription medications
        self.doctor_name = doctor_name
        self.prescription_date = prescription_date
        self.indication = indication
        self.warnings = warnings
        self.expiration_date = expiration_date
        self._validate_dates()  # Validate the date formats during initialization

    def _validate_dates(self):
        """
        Validate the format of the prescription_date and expiration_date.

        Raises:
            ValueError: If the dates are not in the correct format (YYYY-MM-DD).
        """
        # Ensure both dates follow the YYYY-MM-DD format
        try:
            datetime.strptime(self.prescription_date, "%Y-%m-%d")
            datetime.strptime(self.expiration_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format")

    def display_prescription_info(self):
        """
        Display detailed prescription information as a formatted string.

        Returns:
            str: A string containing detailed prescription information.
        """       
        # Combine base medication info with prescription-specific details
        base_info = self.display_info()
        return f"{base_info}, Prescribed by: {self.doctor_name}, Prescription Date: {self.prescription_date}, "\
               f"Indication: {self.indication}, Warnings: {self.warnings}, Expiration Date: {self.expiration_date}"

    def is_expired(self):
        """
        Check if the medication is expired.

        Returns:
            bool: True if the medication is expired, False otherwise.
        """
        try:
            # Get the current date and compare it with the expiration date
            current_date = datetime.now().date()
            expiry_date = datetime.strptime(self.expiration_date, "%Y-%m-%d").date()
            return current_date > expiry_date
        except ValueError:
            # Handle invalid date formats
            print("Error: Invalid date format")
            return True

    def to_dict(self):
        """
        Convert the prescription medication object to a dictionary.

        Returns:
            dict: A dictionary containing the prescription medication details.
        """
        # Start with the base dictionary from the Medication class
        base_dict = super().to_dict()
         # Add prescription-specific attributes to the dictionary
        base_dict.update({
            "doctor_name": self.doctor_name,
            "prescription_date": self.prescription_date,
            "indication": self.indication,
            "warnings": self.warnings,
            "expiration_date": self.expiration_date
        })
        return base_dict
