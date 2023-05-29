# mcc-mnc

mcc-mnc is a tool for matching and retrieving information about Mobile Country Codes (MCC) and Mobile Network Codes (MNC). It allows you to search for MCC-MNC combinations, Country Codes (CC), Public Land Mobile Network (PLMN), or individual MCC, MNC, or CC values to retrieve details about the corresponding mobile network provider. The tool uses a JSON database that maps the MCC-MNC combinations to their associated information such as ISO country codes, country names, and network names.

## Installation

You can install mcc-mnc using pip, the package manager for Python.

```bash
pip install mccmnc
```

## Usage

You can use mcc-mnc to search for MCC-MNC combinations, Country Codes (CC), PLMNs, or individual MCC, MNC, or CC values. Here are some usage examples:

```bash
# Search by Country Code (CC)
python mccmnc.py -cc XXX

# Search by Mobile Country Code (MCC)
python mccmnc.py -mcc XXX

# Search by MCC and MNC
python mccmnc.py -mcc XXX -mnc XXX

# Search by CC, MCC, and MNC
python mccmnc.py -cc XXX -mcc XXX -mnc XXX

# Search by PLMN
python mccmnc.py -plmn XXXXX

# Update the mcc-mnc database
python mccmnc.py -update
```

The `-update` option allows you to download and refresh the local JSON file that mcc-mnc uses for matching.

## Contributing

Contributions, bug reports, and feature requests are welcome! If you would like to contribute to mcc-mnc, please open an issue to discuss your ideas or submit a pull request with your changes.

Please ensure that you update or add relevant tests for your changes.

## License

mcc-mnc is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). Feel free to use, modify, and distribute this project under the terms of this license.