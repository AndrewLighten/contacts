# Contacts

This is a small but useful contact manager.

# Installation

I've created a `setup.py` file that allows for it to be installed using `pip`.

It requires Python 3.7 or later.

To install:

```
$ pip install -e .
Obtaining file:///Users/andrew/Developer/contacts
Installing collected packages: contacts
  Found existing installation: contacts 0.1
    Uninstalling contacts-0.1:
      Successfully uninstalled contacts-0.1
  Running setup.py develop for contacts
Successfully installed contacts
$ 
```

From that point on, you can invoke it with just `contacts` as a command line.

# Contact file

The contact file is currently assumed to be named `contacts.txt` and is located in the running user's home directory (i.e., it's `~/contacts.txt`).

The format of the contact file is simple.

```
name

    keyword: value
    keyword: value
    ...
    - note
    - note
    - ...
```

Here's an example:

```
Roy

    Phone: 0118 999 881 99 9119 7253
    Email: roy@renham-industries.co.uk
    Org:   Renham Industries
    Role:  IT Support
    - Best friend is Moss
```

# Running

To run the contact manager, simply invoke the Python script with one or more patterns. All contacts that match **all** provided patterns will be listed.

A contact is considered to match a pattern if every provided pattern can be found in either the name, a *value*, or a note.

When one or more contacts are found, the script will list how many contacts were found and will list each contact.

For example:

```
$ contacts roy it support

Found 1 contact:

Roy (IT Support, Renham Industries)

    Email ... roy@renham-industries.co.uk
    Phone ... 0118 999 881 99 9119 7253
    - Best friend is Moss

```

Note that the list of keyword/value pairs is sorted in alphabetical order, as is the list of contacts that were found. The notes are printed in the order they were found in the input file (there may be a note that spans multiple lines, so sorting those lines would be weird).

## Command line switches

There are no command line switches of consequence. The switches `--version` and `--help` are supported, but they only do what you'd expect.

```
$ contacts --help
Usage: contacts [OPTIONS] PATTERN...

  The main application.

  Args:     pattern: The pattern to search for.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
$
```

# Special keywords

There is no specific rule describing which keywords are allowed. There are a few that are particularly looked for and treated differently, however.

## `Nickname`

If the `Nickname` keyword is found, it will be searched, but it will _not_ be printed.

For example, consider the following contact:

```
Dr Spock

    Nickname: Doctor
    Email:    spock@enterprise.com
```

This contact will match a search for `doctor spock`, but when it's printed, the result will be:

```
$ contacts doctor spock

Found 1 contact:

Dr Spock

    Email ... spock@enterprise.com
```

The `Doctor` nickname is suppressed from the printed output.

## `DOB`

If the `DOB` keyword is found, it is assumed to represent a date of birth in the form `yyyy-mm-dd`.

For example, consider the following contact:

```
Harry Potter

    Email: harry@hogwarts.co.uk
    DOB:   1980-07-31
```

This indicates that Harry Potter was born on 31st July, 1980.

When the resulting contact is printed, a calculation is done to determine how old someone is based on the current date and their date-of-birth, and this is printed along with the contact.

For example, when run on 26th November 2019:

```
$ contacts hogwarts

Found 1 contact:

Harry Potter

    Email ... harry@hogwarts.co.uk
    DOB ..... 1980-07-31 (aged 39)
```

## `Role` and `Org`

If a contact has either a `Role` or an `Org` keyword, these details are printed along with their name.

Looking at our earlier example:

```
Roy

    Phone: 0118 999 881 99 9119 7253
    Email: roy@renham-industries.co.uk
    Org:   Renham Industries
    Role:  IT Support
    - Best friend is Moss
```

When this is printed, the role (`IT Support`) and the org (`Renham Industries`) are not printed as separate keywords, but they're included in the name. The role is printed first, then the organisation.

For example:

```
$ contacts roy it support

Found 1 contact:

Roy (IT Support, Renham Industries)

    Email ... roy@renham-industries.co.uk
    Phone ... 0118 999 881 99 9119 7253
    - Best friend is Moss

```
