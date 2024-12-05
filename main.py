# main.py
import sys
from pathlib import Path
from user_management.family import FamilyManagement
from user_management.reminder import ReminderSystem
from medication_management.medication import Medication
from medication_management.prescription import PrescriptionMedication

BASE_DIR = Path(__file__).resolve().parent

def initialize_system():
    """
    Initialize the FamilyMedT system.

    Returns:
        tuple: A tuple containing the FamilyManagement and ReminderSystem instances.

    Raises:
        Exception: If there is an error during initialization.
    """
    try:
        # Initialize the reminder system
        reminder_system = ReminderSystem(BASE_DIR)
        # Initialize the family manager with the reminder system
        family_manager = FamilyManagement(BASE_DIR, reminder_system)
        return family_manager, reminder_system
    except Exception as e:
        print(f"Error initializing system: {str(e)}")
        sys.exit(1)

def clean_exit(family_manager):
    """
    Save all data and exit the program.

    Args:
        family_manager (FamilyManagement): The FamilyManagement instance.
    """
    try:
        print("\nSaving data and exiting FamilyMedT...")
        # Check if the family manager has a save method and call it
        if hasattr(family_manager, 'save_all_data'):
            family_manager.save_all_data()
        print("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error during exit: {str(e)}")
        sys.exit(1)

def main():
    """
    Save all data and exit the program.

    Args:
        family_manager (FamilyManagement): The FamilyManagement instance.
    """
    print("Initializing FamilyMedT System...")
    # Initialize the system components
    family_manager, reminder_system = initialize_system()

    while True:
        try:
            # Display any pending reminders
            reminder_system.list_all_reminders()
             # Display the main menu
            print("\n=== FamilyMedT Menu ===")
            print("1. Add Family Member")
            print("2. Switch to Family Member")
            print("3. List Family Members")
            print("4. Add Medication for Current Member")
            print("5. Update Stock for Current Member")
            print("6. Generate Stock Report for Current Member")
            print("7. List Reminders for Current Member")
            print("8. List Prescription Medications")
            print("9. Generate Prescription Report")
            print("10. Delete Family Member")
            print("11. Delete Medication for Current Member")
            print("12. Exit")

            # Get user input
            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                # Add a new family member
                name = input("Enter family member's name: ").strip()
                if name:
                    family_manager.add_member(name)
                else:
                    print("Name cannot be empty.")

            elif choice == "2":
                # Switch to an existing family member
                name = input("Enter family member's name: ").strip()
                if name:
                    family_manager.switch_member(name)
                else:
                    print("Name cannot be empty.")

            elif choice == "3":
                # List all family members
                family_manager.list_members()

            elif choice == "4":
                # Add medication for the current family member
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    try:
                        # Collect medication details from the user
                        name = input("Enter medication name: ").strip()
                        dosage = input("Enter dosage (e.g., 50mg): ").strip()
                        frequency = input("Enter frequency (e.g., twice daily): ").strip()
                        daily_dosage = int(input("Enter daily dosage (number of pills): "))
                        stock = int(input("Enter current stock: "))

                        # Check if it's a prescription medication
                        if input("Is this a prescription medication? (yes/no): ").lower() == 'yes':
                            doctor_name = input("Enter doctor's name: ").strip()
                            prescription_date = input("Enter prescription date (YYYY-MM-DD): ").strip()
                            indication = input("Enter indication: ").strip()
                            warnings = input("Enter warnings: ").strip()
                            expiration_date = input("Enter expiration date (YYYY-MM-DD): ").strip()
                            # Create a PrescriptionMedication object
                            medication = PrescriptionMedication(
                                name=name,
                                dosage=dosage,
                                frequency=frequency,
                                daily_dosage=daily_dosage,
                                stock=stock,
                                doctor_name=doctor_name,
                                prescription_date=prescription_date,
                                indication=indication,
                                warnings=warnings,
                                expiration_date=expiration_date
                            )
                        else:
                            # Create a regular Medication object
                            medication = Medication(
                                name=name,
                                dosage=dosage,
                                frequency=frequency,
                                daily_dosage=daily_dosage,
                                stock=stock
                            )

                        # Add medication to the inventory
                        inventory_manager.add_medication(medication)

                    except ValueError as e:
                        print(f"Invalid input: {str(e)}")
                    except Exception as e:
                        print(f"Error adding medication: {str(e)}")

            elif choice == "5":
                # Update stock for a medication
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    try:
                        med_id = int(input("Enter medication ID: "))
                        quantity = int(input("Enter quantity (negative to remove): "))
                        if inventory_manager.update_stock(med_id, quantity):
                            print("Stock updated successfully.")
                        else:
                            print("Failed to update stock.")
                    except ValueError:
                        print("Please enter valid numbers.")
                else:
                    print("No member selected.")

            elif choice == "6":
                # Generate a stock report for the current member
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    inventory_manager.generate_stock_report()

            elif choice == "7":
                # List reminders for the current member
                if family_manager.current_member:
                    reminder_system.list_reminders(family_manager.current_member)
                else:
                    print("No member selected.")

            elif choice == "8":
                # List all prescription medications for the current member
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    prescriptions = inventory_manager.list_prescription_medications()
                    if prescriptions:
                        for med in prescriptions:
                            print(f"\nMedication ID: {med['id']}")
                            print(f"Name: {med['name']}")
                            print(f"Doctor: {med['doctor']}")
                            print(f"Prescription Date: {med['date']}")
                            print(f"Indication: {med['indication']}")
                            print(f"Warnings: {med['warnings']}")
                            print(f"Expiration Date: {med['expiration_date']}")
                    else:
                        print("No prescription medications found.")

            elif choice == "9":
                # Generate a prescription report for the current member
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    inventory_manager.generate_prescription_report()

            elif choice == "10":
                 # Delete a family member
                name = input("Enter family member's name to delete: ").strip()
                if name:
                    family_manager.delete_member(name)
                else:
                    print("Name cannot be empty.")

            elif choice == "11":
                # Delete a medication for the current member
                inventory_manager = family_manager.get_current_member_inventory()
                if inventory_manager:
                    try:
                        med_id = int(input("Enter medication ID to delete: "))
                        if inventory_manager.delete_medication(med_id):
                            print("Medication deleted successfully.")
                        else:
                            print("Failed to delete medication.")
                    except ValueError:
                        print("Please enter a valid medication ID.")
                else:
                    print("No member selected.")

            elif choice == "12":
                # Exit the program
                clean_exit(family_manager)

            else:
                print("Invalid choice. Please try again.")

        except KeyboardInterrupt:
             # Handle keyboard interrupt (Ctrl+C)
            print("\nReceived interrupt signal.")
            clean_exit(family_manager)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle keyboard interrupt at the program level
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
