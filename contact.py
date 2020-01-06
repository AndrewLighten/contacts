from dataclasses import dataclass
from typing import List

# Separator used when contact has multiple roles or organisations
ROLE_ORG_SEP = " and "


@dataclass
class KeyValue:
    """
    This class represents a key/value pair we've loaded from the contact file.
    """

    # The key
    key: str

    # The value
    value: str

    def __lt__(self, other):
        """
        Sort comparison for key/value pairs.
        
        Args:
            other: The key/value pair to sort against.
        
        Returns:
            bool: True if this key is less than the other key; otherwise, False.
        """
        if self.key == other.key:
            return self.value < other.value
        else:
            return self.key < other.key


@dataclass
class Contact:
    """
    This class represents a single contact we've loaded from the contact file.
    """

    # The contact's name
    name: str

    # The list of keyword/value pairs we've loaded
    kv_pairs: List[KeyValue]

    # The list of notes we've loaded
    notes: List[str]

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
        for kv in self.kv_pairs:
            if pattern in kv.value.lower():
                return True

        # Check the notes
        for note in self.notes:
            if pattern in note.lower():
                return True

        # Not there
        return False

    def get(self, key: str) -> List[KeyValue]:
        """
        Get the values for a given key.
        
        Args:
            key: The key whose value we want.
        
        Returns:
            [KeyValue]: The values associated with the key.
        """

        # Get the list of values with this key
        return [x for x in self.kv_pairs if x.key == key]

    def org_and_role(self) -> str:
        """
        Get a representation of a person's organisation and role.
        
        If either the "Org" or "Role" keyword is found, the result is a string
        formatted as "([Role], [Org])".
        
        Returns:
            str: The contact's role and organisation.
        """

        # Find the organisations and/or roles
        org_list = [x.value for x in self.kv_pairs if x.key == "Org"]
        role_list = [x.value for x in self.kv_pairs if x.key == "Role"]

        # Sort each list
        org_list.sort()
        role_list.sort()

        # Format as required
        if org_list and role_list:
            return (
                " ("
                + ROLE_ORG_SEP.join(role_list)
                + " at "
                + ROLE_ORG_SEP.join(org_list)
                + ")"
            )
        elif org_list:
            return " (" + ROLE_ORG_SEP.join(org_list) + ")"
        elif role_list:
            return " (" + ROLE_ORG_SEP.join(role_list) + ")"
        return ""
