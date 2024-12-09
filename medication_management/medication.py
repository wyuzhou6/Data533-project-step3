# medication.py
class Medication:
    """
    A class representing a medication.

    Attributes:
        name (str): The name of the medication.
        dosage (str): The dosage information (e.g., "500mg").
        frequency (str): The frequency of intake (e.g., "2 times/day")
        daily_dosage (int): The daily dosage (number of units per day).
        stock (int): The current stock level.
    """
    def __init__(self, name, dosage, frequency, daily_dosage, stock):
        """
        Initialize a Medication object.

        Args:
            name (str): The name of the medication.
            dosage (str): The dosage information (e.g., "500mg").
            frequency (str): The frequency of intake (e.g., "2 times/day").
            daily_dosage (int): The daily dosage (number of units per day).
            stock (int): The current stock level.
        """
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        self.daily_dosage = daily_dosage
        self.stock = stock

    def calculate_days_left(self):
        """
        Calculate the remaining days of stock based on daily dosage.

        Returns:
            int: The number of days of stock left.

        Raises:
            ValueError: If daily_dosage is not a positive integer.
        """
        # Ensure that daily_dosage is a valid positive integer.
        if not isinstance(self.daily_dosage, int) or self.daily_dosage <= 0:
            raise ValueError("Daily dosage must be a positive integer.")
        return self.stock // self.daily_dosage  #  Calculate the remaining days of stock.

    def display_info(self):
        """
        Display medication information as a formatted string.

        Returns:
            str: A string containing medication details.
        """
         # Format and return a string with all medication details.
        return f"Medication: {self.name}, Dosage: {self.dosage}, Frequency: {self.frequency}, Daily Dosage: {self.daily_dosage}, Stock: {self.stock}"

    def update_stock(self, quantity):
        """
        Update the stock of the medication.

        Args:
            quantity (int): The quantity to add (positive) or remove (negative).

        Returns:
            bool: True if the stock update was successful, False otherwise.

        Raises:
            ValueError: If quantity is not an integer.
        """
        # Check if the quantity is a valid integer.
        if not isinstance(quantity, int):
            raise ValueError("Quantity must be an integer.")
        if self.stock + quantity < 0:   # Verify that there is enough stock to remove the requested amount
            print(f"Not enough stock to remove. Current stock: {self.stock}, Requested: {abs(quantity)}")
            return False
        self.stock += quantity  # Update the stock level.
        return True

    def to_dict(self):
        """
        Convert the medication object to a dictionary.

        Returns:
            dict: A dictionary containing the medication details.
        """
        # Convert the medication's attributes into a dictionary format.
        return {
            "name": self.name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "daily_dosage": self.daily_dosage,
            "stock": self.stock
        }

    def __repr__(self):
        """
        Return a string representation of the Medication object.

        Returns: A string representing the medication.
        """
        # Provide a concise string representation of the medication object
        # for debugging or logging purposes
        return f"Medication(name={self.name}, dosage={self.dosage}, frequency={self.frequency}, daily_dosage={self.daily_dosage}, stock={self.stock})"
