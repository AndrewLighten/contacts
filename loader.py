from contact import Contact, KeyValue
from typing import List
from os.path import expanduser

# Contact file
CONTACT_FILE = "~/contacts.txt"


def load_contacts() -> List[Contact]:
    """
    Load a list of contacts from a file.
    
    Returns:
        [Contact]: The list of loaded contacts.
    """

    # Find the contact file
    contact_file = expanduser(CONTACT_FILE)

    # Initialise
    contact_list = []
    current_contact = None

    # Open and read the file
    with open(contact_file) as file:

        # Visit each line
        for line in file.readlines():

            # Ignore blank lines
            if not (content := line.rstrip()):
                continue

            # If it doesn't start with whitespace, it's a new contact
            if not str.isspace(content[0]):
                current_contact = Contact(name=content, kv_pairs=[], notes=[])
                contact_list.append(current_contact)
                continue

            # Make sure we're in a contact
            if not current_contact:
                print(f"No current contact -- review file format")
                continue

            # Trim string
            trimmed = content.lstrip()

            # A note?
            if trimmed.startswith("- "):
                note = trimmed[2:].strip()
                if note:
                    current_contact.notes.append(note)

            # No, must be keyword:value
            else:
                if len(words := trimmed.split(":", 1)) != 2:
                    print(f"Bad contact details ({trimmed}) -- ignored")
                else:
                    key = words[0].strip()
                    value = words[1].strip()
                    current_contact.kv_pairs.append(KeyValue(key=key, value=value))

    # Return the list of contacts
    return contact_list
