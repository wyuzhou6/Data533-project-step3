# Import necessary modules
import pandas as pd  # For handling CSV files and data manipulation
from pathlib import Path  # For handling file paths
from medication_management.inventory import InventoryManagement  # For managing inventory of medications

class FamilyManagement:
    """
    A class to manage family members and their medication inventories. 
    Provides functionality for adding, removing, and switching between family members, 
    as well as checking and managing medication inventory.
    """

    def __init__(self, base_dir, reminder_system):
        """
        Initialize the FamilyManagement class.
        
        Args:
            base_dir (Path): The base directory for storing family data.
            reminder_system (object): An external system for managing reminders and alerts.
        """
        self.base_dir = base_dir  # Base directory for family data
        self.reminder_system = reminder_system  # Reminder system for managing alerts
        self.data_dir = self.base_dir / "data"  # Directory for storing family data files
        self.data_dir.mkdir(exist_ok=True)  # Create the data directory if it doesn't exist
        self.members_file = self.data_dir / "members.csv"  # File to store family member data
        self.members = {}  # Dictionary to store family members and their inventory managers
        self.current_member = None  # The currently selected family member
        self._load_members()  # Load existing family member data from file

    def _load_members(self):
        """
        Load family members from the CSV file.
        If the file doesn't exist, create an empty file with a 'name' column.
        """
        if not self.members_file.exists():
            # Create an empty CSV file if it doesn't exist
            df = pd.DataFrame(columns=['name'])
            df.to_csv(self.members_file, index=False)
            return

        try:
            # Load the members from the CSV file
            df = pd.read_csv(self.members_file)
            if not df.empty:
                for _, row in df.iterrows():
                    # Create an InventoryManagement instance for each member
                    self.members[row['name']] = InventoryManagement(
                        row['name'], self.base_dir, self.reminder_system
                    )
        except Exception as e:
            # Handle errors and recreate an empty file if needed
            print(f"Error loading members: {str(e)}")
            df = pd.DataFrame(columns=['name'])
            df.to_csv(self.members_file, index=False)

    def save_all_data(self):
        """
        Save all family member data to the CSV file and their respective inventory files.
        
        Returns:
            bool: True if save operation was successful, False otherwise.
        """
        try:
            # Save family members' names to the CSV file
            df = pd.DataFrame({'name': list(self.members.keys())})
            df.to_csv(self.members_file, index=False)

            # Save each member's inventory data
            for member_name, inventory in self.members.items():
                inventory._save_inventory()

            print("All data saved successfully")
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def add_member(self, name):
        """
        Add a new family member.
        
        Args:
            name (str): The name of the new family member.
        
        Returns:
            bool: True if the member was added successfully, False otherwise.
        """
        if not name:
            raise ValueError("Name cannot be empty")

        if name in self.members:
            print(f"Member {name} already exists.")
            return False

        # Create a new InventoryManagement instance for the member
        self.members[name] = InventoryManagement(name, self.base_dir, self.reminder_system)
        self.save_all_data()  # Save updated data
        print(f"Family member '{name}' added successfully.")
        return True

    def switch_member(self, name):
        """
        Switch the current active family member.
        
        Args:
            name (str): The name of the family member to switch to.
        
        Returns:
            bool: True if the switch was successful, False otherwise.
        """
        if name in self.members:
            self.current_member = name  # Set the current member
            print(f"Switched to family member: {name}")

            # Check for low stock medications for the new member
            inventory_manager = self.get_current_member_inventory()
            if inventory_manager:
                low_stock_warnings = inventory_manager.check_low_stock()
                if low_stock_warnings:
                    # Notify about low stock through the reminder system
                    self.reminder_system.check_alerts(name, low_stock_warnings)
            return True
        
        print(f"Family member '{name}' not found.")
        return False

    def list_members(self):
        """
        List all registered family members.
        """
        if not self.members:
            print("No family members registered.")
            return

        print("\nRegistered family members:")
        for name in self.members:
            # Mark the current member
            if name == self.current_member:
                print(f"- {name} (current)")
            else:
                print(f"- {name}")

    def delete_member(self, name):
        """
        Delete a family member and their associated data.
        
        Args:
            name (str): The name of the member to delete.
        
        Returns:
            bool: True if the member was deleted successfully, False otherwise.
        """
        if name not in self.members:
            print(f"Family member '{name}' not found.")
            return False

        # Delete the member's inventory files if they exist
        inventory = self.members[name]
        if hasattr(inventory, 'inventory_file') and inventory.inventory_file.exists():
            inventory.inventory_file.unlink()
        if hasattr(inventory, 'history_file') and inventory.history_file.exists():
            inventory.history_file.unlink()

        # Remove the member from the dictionary
        del self.members[name]
        if self.current_member == name:
            self.current_member = None  # Clear the current member if it was the one deleted

        # Clear all reminders for the deleted member
        self.reminder_system.clear_all_reminders(name)

        self.save_all_data()  # Save updated data
        print(f"Family member '{name}' and associated data deleted successfully.")
        return True

    def get_current_member_inventory(self):
        """
        Get the inventory manager for the currently selected family member.
        
        Returns:
            InventoryManagement: The inventory manager for the current member, or None if no member is selected.
        """
        if not self.current_member:
            print("No family member selected.")
            return None
        return self.members[self.current_member]

    def get_all_low_stock(self):
        """
        Retrieve low stock warnings for all family members.
        
        Returns:
            list: A list of tuples containing member name, medication ID, medication name, and days left.
        """
        low_stock_warnings = []
        for member_name, inventory in self.members.items():
            low_stock_meds = inventory.check_low_stock()
            for med_id, med_name, days_left in low_stock_meds:
                low_stock_warnings.append((member_name, med_id, med_name, days_left))
        return low_stock_warnings
