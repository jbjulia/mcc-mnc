# mcc-mnc

mcc-mnc is a tool for matching and retrieving information about Mobile Country Codes (MCC) and Mobile Network Codes (
MNC). It allows you to search for MCC-MNC combinations, Country Codes (CC), Public Land Mobile Network (PLMN), or
individual MCC, MNC, or CC values to retrieve details about the corresponding mobile network provider. The tool uses a
JSON database that maps the MCC-MNC combinations to their associated information such as ISO country codes, country
names, and network names.

## Installation

You can install mcc-mnc using pip, the Python package manager.

```bash
pip install mccmnc
```

## Usage

You can use mcc-mnc to search for MCC-MNC combinations, Country Codes (CC), PLMNs, or individual MCC, MNC, or CC values.
Here are some usage examples:

```bash
# Search by Country Code (CC)
mccmnc -cc XXX

# Search by Mobile Country Code (MCC)
mccmnc -mcc XXX

# Search by MCC and MNC
mccmnc -mcc XXX -mnc XXX

# Search by CC, MCC, and MNC
mccmnc -cc XXX -mcc XXX -mnc XXX

# Search by PLMN
mccmnc -plmn XXXXX

# Update the mcc-mnc database
mccmnc -update
```

The `-update` option allows you to download and refresh the local JSON file that mcc-mnc uses for matching.

## Python Usage

You can also use `mccmnc` within your Python programs. First, make sure it's installed in your Python environment, then
you can import it and use its functions. Here's an example:

```python
from mccmnc import find_matches, print_matches, update

# Example of searching by MCC and MNC
matches = find_matches(user_mcc="123", user_mnc="45")
if matches:
    print_matches(matches)
else:
    print("No match found.")

# Example of updating the database
update()
```

These examples demonstrate how to use `find_matches` to search for MCC-MNC combinations and `print_matches` to print out
the details of the matches. The `update` function is used to update the MCC-MNC database.

## Contributing

Contributions, bug reports, and feature requests are welcome! If you would like to contribute to mcc-mnc, please open an
issue to discuss your ideas or submit a pull request with your changes.

Please ensure that you update or add relevant tests for your changes.

## License

mcc-mnc is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). Feel free to use, modify, and
distribute this project under the terms of this license.