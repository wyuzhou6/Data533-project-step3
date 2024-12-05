# Import necessary modules
import pandas as pd  # For handling CSV files and data manipulation
from pathlib import Path  # For handling file paths

class ReminderSystem:
    """
    A system to manage reminders for family members' medications.
    Provides functionality to set, clear, and list reminders, as well as save and load them from a CSV file.
    """

    def __init__(self, base_dir):
        """
        Initialize the ReminderSystem class.

        Args:
            base_dir (str or Path): Base directory where reminder data is stored.
        """
        self.base_dir = Path(base_dir)  # Ensure base_dir is a Path object
        self.data_dir = self.base_dir / "data"  # Directory for storing reminder data
        self.data_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist
        self.reminders_file = self.data_dir / "reminders.csv"  # File for storing reminders

        # Structure to hold reminders, organized by member name
        # Example structure: { "member_name": {med_id: message, ...}, ... }
        self.reminders = {}
        self._load_reminders()  # Load existing reminders from file

    def _load_reminders(self):
        """
        Load reminders from the CSV file into the `self.reminders` dictionary.
        If the file doesn't exist, create a new empty file.
        """
        if not self.reminders_file.exists():
            # Create a new empty CSV file with required columns
            df = pd.DataFrame(columns=['member', 'med_id', 'message'])
            df.to_csv(self.reminders_file, index=False)
            return

        try:
            # Read reminders from the CSV file
            df = pd.read_csv(self.reminders_file)
            if not df.empty:
                # Populate the reminders dictionary
                for _, row in df.iterrows():
                    member = row['member']
                    med_id = int(row['med_id'])  # Ensure medication ID is stored as an integer
                    message = row['message']
                    if member not in self.reminders:
                        self.reminders[member] = {}
                    self.reminders[member][med_id] = message
        except Exception as e:
            # Handle errors during loading
            print(f"Error loading reminders: {str(e)}")
            df = pd.DataFrame(columns=['member', 'med_id', 'message'])
            df.to_csv(self.reminders_file, index=False)

    def _save_reminders(self):
        """
        Save the current reminders to the CSV file for persistence.
        """
        try:
            # Convert reminders dictionary into a list of rows for saving
            data = []
            for member, member_reminders in self.reminders.items():
                for med_id, message in member_reminders.items():
                    data.append({
                        'member': member,
                        'med_id': med_id,
                        'message': message
                    })

            # Save the data into the reminders CSV file
            df = pd.DataFrame(data)
            df.to_csv(self.reminders_file, index=False)
            print("Reminders saved successfully")
        except Exception as e:
            print(f"Error saving reminders: {str(e)}")

    def set_reminder(self, member, med_id, message):
        """
        Set a reminder for a specific medication for a family member.

        Args:
            member (str): The name of the family member.
            med_id (int): The ID of the medication.
            message (str): The reminder message.
        """
        if member not in self.reminders:
            self.reminders[member] = {}
        self.reminders[member][med_id] = message
        self._save_reminders()

    def clear_reminder(self, member, med_id):
        """
        Clear a specific reminder for a family member.

        Args:
            member (str): The name of the family member.
            med_id (int): The ID of the medication whose reminder should be cleared.
        """
        if member in self.reminders and med_id in self.reminders[member]:
            del self.reminders[member][med_id]
            self._save_reminders()
            print(f"Cleared reminder for {member} - Medication ID {med_id}.")

    def check_alerts(self, member, low_stock_warnings):
        """
        Check and set low stock alerts for a family member based on provided warnings.

        Args:
            member (str): The name of the family member.
            low_stock_warnings (list of tuples): A list of tuples containing:
                - med_id (int): The ID of the medication.
                - med_name (str): The name of the medication.
                - days_left (int): The number of days left before running out of stock.
        """
        if low_stock_warnings:
            for med_id, med_name, days_left in low_stock_warnings:
                message = f"Low stock alert for {med_name} (ID {med_id})! Only {days_left} days left."
                self.set_reminder(member, med_id, message)
                print(message)  # Print the alert for immediate feedback

    def list_reminders(self, member):
        """
        List all active reminders for a specific family member.

        Args:
            member (str): The name of the family member.
        """
        if member not in self.reminders or not self.reminders[member]:
            print(f"\nNo active reminders for {member}.")
            return

        print(f"\nActive reminders for {member}:")
        for med_id, message in self.reminders[member].items():
            print(f"ID: {med_id}, Message: {message}")

    def list_all_reminders(self):
        """
        List all active reminders for all family members.
        """
        if not any(reminders for reminders in self.reminders.values()):
            print("\nNo active reminders.")
            return

        print("\n=== Active Reminders for All Members ===")
        for member, member_reminders in self.reminders.items():
            if member_reminders:
                print(f"\nReminders for {member}:")
                for med_id, message in member_reminders.items():
                    print(f"ID: {med_id}, Message: {message}")

    def clear_all_reminders(self, member):
        """
        Clear all reminders for a specific family member.

        Args:
            member (str): The name of the family member.
        """
        if member in self.reminders:
            self.reminders[member] = {}
            self._save_reminders()
            print(f"All reminders cleared for {member}.")
