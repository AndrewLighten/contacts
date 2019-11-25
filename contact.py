from dataclasses import dataclass
from relativedelta import relativedelta
import datetime


@dataclass
class Contact:
    """
    This class represents a single contact we've loaded from the contact file.
    """

    # The contact's name
    name: str

    # The list of keyword/value pairs we've loaded
    kv_pairs: {}

    # The list of notes we've loaded
    notes: []

    def matches(self, pattern: str) -> bool:
        """
        Check whether this contact matches the specified pattern.
        
        The pattern is checked against the name, the value of all keyword/value
        pairs, and the list of notes.
        
        Args:
            pattern: The pattern to match.
        
        Returns:
            bool: True if this contact matches the pattern; otherwise, False.
        """

        # Check the name
        if pattern in self.name.lower():
            return True

        # Check the values
        for key in self.kv_pairs:
            if pattern in self.kv_pairs[key].lower():
                return True

        # Check the notes
        for note in self.notes:
            if pattern in note.lower():
                return True

        # Not there
        return False

    def get(self, key: str) -> str:
        """
        Get the value for a given key.
        
        Args:
            key: The key whose value we want.
        
        Returns:
            str: The value associated with the key.
        """

        # Find the raw value
        value = self.kv_pairs.get(key)
        if not value:
            return None

        # Intercept date-of-birth and add in their age
        if key.lower() == "dob":
            value = value + self._calculate_age(value)

        # Done
        return value

    def org_and_role(self) -> str:
        """
        Get a representation of a person's organisation and role.
        
        If either the "Org" or "Role" keyword is found, the result is a string
        formatted as "([Role], [Org])".
        
        Returns:
            str: The contact's role and organisation.
        """

        # Find the organisation and/or role
        org = self.kv_pairs.get("Org")
        role = self.kv_pairs.get("Role")
        if org and role:
            return " (" + role + ", " + org + ")"
        if org:
            return " (" + org + ")"
        if role:
            return " (" + role + ")"
        return ""

    def _calculate_age(self, dob: str) -> str:
        """
        Calculate someone's age given their date-of-birth.
        
        Args:
            dob: The date of birth, formatted as yyyy-mm-dd.
        
        Returns:
            str: A text description of the person's age.
        """

        # Catch problems
        try:

            # Make sure the date-of-birth is formatted ok.
            birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d")

            # Find today's date
            today = datetime.datetime.today()

            # Calculate difference
            age = relativedelta(today, birth_date).years
            return f" (aged {age})"

        # Parse problem -- ignore it
        except ValueError:
            return ""
