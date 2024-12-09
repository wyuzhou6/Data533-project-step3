# inventory.py
import os
import pandas as pd
from pathlib import Path
from medication_management.medication import Medication
from medication_management.prescription import PrescriptionMedication

class InventoryManagement:
    """
    A class to manage medication inventory for a specific member.
    
    Attributes:
        member_name (str): Name of the member.
        base_dir (Path): Base directory to store data files.
        reminder_system (object): Optional reminder system for low stock alerts.
    """    
    def __init__(self, member_name, base_dir, reminder_system=None):
        """
        Initialize the InventoryManagement class.

        Args:
            member_name (str): Name of the member.
            base_dir (str): Base directory to store data files.
            reminder_system (object, optional): Reminder system for alerts.
        """
        self.member_name = member_name
        self.base_dir = Path(base_dir)
        self.reminder_system = reminder_system
        
        # Ensure the data directory exists
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.inventory_file = self.data_dir / f"{member_name}_inventory.csv"   # Define paths for inventory and history files
        self.history_file = self.data_dir / f"{member_name}_history.csv"

        self.medications = {} # Initialize medication dictionary and ID tracker.
        self.next_med_id = 1
        self._load_inventory() # Load inventory if it exists

    def _load_inventory(self):
        """
        Load inventory data from a CSV file. If the file doesn't exist,
        create an empty inventory file.
        """
        if not self.inventory_file.exists():
            self._create_empty_inventory()
            return

        try:
            df = pd.read_csv(self.inventory_file)
            if df.empty:
                self._create_empty_inventory()
                return
            # Load medications from the CSV file
            for _, row in df.iterrows():
                try:
                    if row['is_prescription']:  # Differentiate between prescription and non-prescription medications
                        med = PrescriptionMedication(
                            name=row['name'],
                            dosage=row['dosage'],
                            frequency=row['frequency'],
                            daily_dosage=row['daily_dosage'],
                            stock=row['stock'],
                            doctor_name=row['doctor_name'],
                            prescription_date=row['prescription_date'],
                            indication=row['indication'],
                            warnings=row['warnings'],
                            expiration_date=row['expiration_date']
                        )
                    else:
                        med = Medication(
                            name=row['name'],
                            dosage=row['dosage'],
                            frequency=row['frequency'],
                            daily_dosage=row['daily_dosage'],
                            stock=row['stock']
                        )
                    self.medications[int(row['med_id'])] = med
                except Exception as e:
                    print(f"Error loading medication: {str(e)}")
                    continue

            if not df.empty:     # Update the next medication ID
                self.next_med_id = df['med_id'].max() + 1

        except Exception as e:
            print(f"Error loading inventory: {str(e)}")
            self._create_empty_inventory()

    def _create_empty_inventory(self):
        """Create an empty inventory file with predefined columns."""
        columns = [
            'med_id', 'name', 'dosage', 'frequency', 'daily_dosage',
            'stock', 'is_prescription', 'doctor_name', 'prescription_date',
            'indication', 'warnings', 'expiration_date'
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(self.inventory_file, index=False)

    def _save_inventory(self):
        """
        Save the current inventory to a CSV file.
        """
        try:
            data = []
            for med_id, med in self.medications.items():
                med_data = med.to_dict()
                med_data['med_id'] = med_id
                med_data['is_prescription'] = isinstance(med, PrescriptionMedication)
                data.append(med_data)

            if not data:
                return

            df = pd.DataFrame(data)
            df.to_csv(self.inventory_file, index=False)
            print(f"Inventory for {self.member_name} saved successfully.")

        except Exception as e:
            print(f"Error saving inventory: {str(e)}")

    def add_medication(self, medication):
        """
        Add a new medication to the inventory.

        Args:
            medication (Medication): The medication object to add.

        Returns:
            int: The ID of the added medication.
        """
        med_id = self.next_med_id
        self.medications[med_id] = medication
        self.next_med_id += 1

        self._save_inventory()
        print(f"Added medication {medication.name} with ID {med_id}")
        
        # Check stock and set reminders if applicable
        try:
            days_left = medication.calculate_days_left()
            if days_left <= 3 and self.reminder_system:
                self.reminder_system.set_reminder(
                    self.member_name,
                    med_id,
                    f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                )
        except Exception as e:
            print(f"Error checking stock for new medication: {str(e)}")
        
        return med_id

    def update_stock(self, med_id, quantity):
        """
        Update the stock of a medication.

        Args:
            med_id (int): The ID of the medication to update.
            quantity (int): The amount to add to the stock.

        Returns:
            bool: True if successful, False otherwise.
        """
        if med_id not in self.medications:
            print(f"Medication ID {med_id} not found.")
            return False

        medication = self.medications[med_id]
        if medication.update_stock(quantity):
            self._save_inventory()
            print(f"Updated stock for {medication.name} (ID {med_id}) by {quantity}")

             # Check updated stock status and set or clear reminders
            try:
                days_left = medication.calculate_days_left()
                if days_left <= 3 and self.reminder_system: # Set reminders during low stock check
                    self.reminder_system.set_reminder(
                        self.member_name,
                        med_id,
                        f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                    )
                elif days_left > 3 and self.reminder_system:
                    self.reminder_system.clear_reminder(self.member_name, med_id)
            except Exception as e:
                print(f"Error checking stock after update: {str(e)}")

            return True

        print(f"Failed to update stock for {medication.name} (ID {med_id})")
        return False

    def delete_medication(self, med_id):
        """
        Delete a medication from the inventory.

        Args:
            med_id (int): The ID of the medication to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        if med_id not in self.medications:
            print(f"Medication ID {med_id} not found.")
            return False

        deleted_med = self.medications.pop(med_id)
        self._save_inventory()

        if self.reminder_system:
            self.reminder_system.clear_reminder(self.member_name, med_id)

        print(f"Medication '{deleted_med.name}' (ID {med_id}) deleted successfully.")
        return True

    def check_low_stock(self):
        """
        Check for medications with low stock.

        Returns:
            list: A list of tuples containing medication ID, name, and days left.
        """
        low_stock = []
        for med_id, medication in self.medications.items():
            try:
                days_left = medication.calculate_days_left()
                if days_left <= 3:
                    low_stock.append((med_id, medication.name, days_left))
                     # Set reminders during low stock check
                    if self.reminder_system:
                        self.reminder_system.set_reminder(
                            self.member_name,
                            med_id,
                            f"Low stock alert for {medication.name} (ID {med_id})! Only {days_left} days left."
                        )
            except Exception as e:
                print(f"Error checking stock for medication {med_id}: {str(e)}")
                continue

        return low_stock

    def generate_stock_report(self):
        """
        Generate a stock report for all medications.
        """
        if not self.medications:
            print(f"No medications found for {self.member_name}.")
            return

        print(f"\nStock Report for {self.member_name}:")
        print(f"{'ID':<5} {'Name':<20} {'Stock':<10} {'Days Left':<10}")
        print("-" * 50)

        for med_id, medication in self.medications.items():
            days_left = medication.calculate_days_left() or "N/A"
            print(f"{med_id:<5} {medication.name:<20} {medication.stock:<10} {days_left:<10}")

    def generate_prescription_report(self):
        """
        Generate a report for prescription medications.
        """
        prescriptions = self.list_prescription_medications()
        if not prescriptions:
            print(f"No prescription medications found for {self.member_name}.")
            return

        print(f"\nPrescription Report for {self.member_name}:")
        print(f"{'ID':<5} {'Name':<20} {'Doctor':<15} {'Date':<12} {'Expiration':<12}")
        print("-" * 80)

        for med in prescriptions:
            print(f"{med['id']:<5} {med['name']:<20} {med['doctor']:<15} {med['date']:<12} {med['expiration_date']:<12}")

    def list_prescription_medications(self):
        """        
        List all prescription medications.
        Returns:
            list: A list of dictionaries with prescription details.
        """
        prescriptions = [
            {
                "id": med_id,
                "name": med.name,
                "doctor": getattr(med, 'doctor_name', 'N/A'),
                "date": getattr(med, 'prescription_date', 'N/A'),
                "indication": getattr(med, 'indication', 'N/A'),
                "warnings": getattr(med, 'warnings', 'N/A'),
                "expiration_date": getattr(med, 'expiration_date', 'N/A')
            }
            for med_id, med in self.medications.items()
            if isinstance(med, PrescriptionMedication)
        ]
        return prescriptions
