from loader import load_contacts
from contact import Contact
from filter import filter_contacts
from termcolor import colored
import click

# List of keys we ignore in printing results
IGNORED_KEYS = ["Nickname", "Role", "Org"]

# Company keys that we print separately
COMPANY_KEYS = ["Role", "Org"]


@click.command()
@click.version_option()
@click.argument("pattern", nargs=-1, required=True)
def main(pattern: (str)):
    """
    The main application.

    Args:
        pattern: The pattern to search for.
    """

    # Load the list of contacts
    contacts = load_contacts()

    # Search for the contacts that match the user's input
    filtered = filter_contacts(contacts, pattern)
    if filtered:
        print_contacts(filtered)
    else:
        print(f"No matching contacts found")


# -----------------------------------------------------------------------------


def print_contacts(contacts: [Contact]):
    """
    Print the list of matching contacts.
    
    Args:
        contacts: The list of contacts we found.
    """

    # Print the match count
    _print_match_count(len(contacts))

    # Sort the filtered contacts by name
    contacts.sort(key=lambda x: x.name)

    # Find the longest keyword in all contacts (we use this for formatting)
    longest_key = _find_longest_key(contacts)

    # Print the contacts
    for contact in contacts:
        _print_contact(contact, longest_key)

    # Finish off
    print("")


def _print_match_count(match_count: int):
    """
    Print the number of matches we got.
    
    Args:
        match_count: The number of matches we got.
    """

    match_pluralisation = "contact" if match_count == 1 else "contacts"
    print("")
    print(colored(f"Found {match_count} {match_pluralisation}:", "green", attrs=["bold"]))


def _print_contact(contact: Contact, longest_key: int):
    """
    Print a contact's details.
    
    Args:
        contact:     The contact to print.
        longest_key: The longest keyword in all matching contacts.
    """
    _print_name(contact)
    _print_keywords(contact, longest_key)
    _print_notes(contact)


def _print_name(contact: Contact):
    """
    Print a contact's name.
    
    Args:
        contact: The contact to print details for.
    """

    # Find the contact's organisation and role.
    org_and_role = contact.org_and_role()

    # Print the name.
    print("")
    print(colored(contact.name, "blue", attrs=["bold"]), end="")
    if org_and_role:
        print(colored(org_and_role, "blue"))
    else:
        print("")
    print("")


def _print_keywords(contact: Contact, longest_key: int):
    """
    Print a contact's keywords.
    
    Args:
        contact:     The contact to print.
        longest_key: The longest keyword in all matching contacts.
    """

    # Get the key/value pairs as a list, then sort them
    kv_pairs = list(contact.kv_pairs.keys())
    kv_pairs.sort()

    # Visit the list of keys
    for key in kv_pairs:

        # Ignore those in our ignore list
        if key in IGNORED_KEYS:
            continue

        # Find the value, determine the required spacing, then print
        value = contact.get(key)
        spacing = longest_key - len(key)
        dots = "." * (spacing + 3)
        print(colored(f"   {key} {dots} {value}", "white"))


def _print_notes(contact: Contact):
    """
    Print a contact's notes.
    
    Args:
        contact: The contact to print details for.
    """

    # Print notes
    for note in contact.notes:
        print(colored(f"   - {note}", "yellow"))


def _find_longest_key(contacts: [Contact]) -> int:
    """
    Find the longest key in the details we're printing for a list of contacts.
    
    Args:
        contacts: The list of contacts
    
    Returns:
        int: The length of the longest key we print
    """
    longest = 0
    for contact in contacts:
        for key in contact.kv_pairs:
            if key not in IGNORED_KEYS:
                longest = max(longest, len(key))
    return longest
