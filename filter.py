from contact import Contact


def filter_contacts(contacts: [Contact], pattern: (str)) -> [Contact]:
    """
    Filter a collection of contacts to return only those that match all
    provided pattern strings.
    
    Args:
        contacts: The contacts to filter
        pattern:  The patterns to match
    
    Returns:
        [Contact]: The list of filtered contacts
    """

    # Filtered contact list
    filtered_list = []

    # Visit each contact and keep those that match every pattern
    for contact in contacts:
        matches_all = True
        for p in pattern:
            if not contact.matches(p.lower()):
                matches_all = False
        if matches_all:
            filtered_list.append(contact)

    # Done
    return filtered_list
