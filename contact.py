from dataclasses import dataclass


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
