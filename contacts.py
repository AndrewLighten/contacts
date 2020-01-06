from loader import load_contacts
from contact import Contact
from filter import filter_contacts
from termcolor import colored
from relativedelta import relativedelta
from typing import List

import datetime
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


def print_contacts(contacts: List[Contact]):
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
    print(
        colored(f"Found {match_count} {match_pluralisation}:", "green", attrs=["bold"])
    )


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

    # Get a copy of the key/value list, then sort it
    kv_pairs = list(contact.kv_pairs)
    kv_pairs.sort()

    # Visit the list of keys
    for kv in kv_pairs:

        # Ignore those in our ignore list
        if kv.key in IGNORED_KEYS:
            continue

        # Format the key
        formatted_key = kv.key.upper() if len(kv.key) <= 3 else kv.key.capitalize()

        # Format the value
        formatted_value = kv.value
        if kv.key.lower() == "dob":
            formatted_value = formatted_value + _calculate_age(kv.value)

        # Find the value, determine the required spacing, then print
        spacing = longest_key - len(kv.key)
        dots = "." * (spacing + 3)
        print(colored(f"   {formatted_key} {dots} {formatted_value}", "white"))


def _print_notes(contact: Contact):
    """
    Print a contact's notes.
    
    Args:
        contact: The contact to print details for.
    """

    # Print notes
    for note in contact.notes:
        print(colored(f"   - {note}", "yellow"))


def _find_longest_key(contacts: List[Contact]) -> int:
    """
    Find the longest key in the details we're printing for a list of contacts.
    
    Args:
        contacts: The list of contacts
    
    Returns:
        int: The length of the longest key we print
    """
    longest = 0
    for contact in contacts:
        for kv in contact.kv_pairs:
            if kv.key not in IGNORED_KEYS:
                longest = max(longest, len(kv.key))
    return longest


def _calculate_age(dob: str) -> str:
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


if __name__ == "__main__":
    main(["fred"])
