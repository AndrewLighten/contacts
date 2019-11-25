from loader import load_contacts
from contact import Contact
from filter import filter_contacts
from termcolor import colored
import click

# List of keys we ignore in printing results
IGNORED_KEYS = ["Nickname"]


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


def print_contacts(contacts: [Contact]):
    """
    Prinbt the list of matching contacts.
    
    [extended_summary]
    
    Args:
        contacts: The list of contacts we found.
    """

    # How many did we find?
    match_count = len(contacts)
    match_plural = "contact" if match_count == 1 else "contacts"
    print("")
    print(colored(f"Found {match_count} {match_plural}:", "green", attrs=["bold"]))

    # Find the longest key in all matching contacts
    longest_key = _find_longest_key(contacts)

    # Sort the filtered contacts by name
    contacts.sort(key=lambda x: x.name)

    # Print the resulting contacts
    for contact in contacts:

        # Print the contact's name
        print("")
        print(colored(contact.name, "blue", attrs=["bold", "underline"]))
        print("")

        # Print the key/value pairs
        kv_pairs = list(contact.kv_pairs.keys())
        kv_pairs.sort()
        for key in kv_pairs:
            if key in IGNORED_KEYS:
                continue
            value = contact.get(key)
            spacing = longest_key - len(key)
            dots = "." * (spacing + 3)
            print(colored(f"   {key} {dots} {value}", "white"))

        # Print notes
        for note in contact.notes:
            print(colored(f"   - {note}", "yellow"))

    # Finish off
    print("")


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
