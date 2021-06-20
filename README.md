# MCC-MNC

A Mobile Country Code (MCC) is used in wireless networks (GSM, CDMA, UMTS, etc.) to identify the country in which a
mobile subscriber (MS)
belongs to. To uniquely identify a mobile subscriber's network provider the MCC is combined with a Mobile Network Code (
MNC). The combination of MCC and MNC is called the Home Network Identity (HNI), and is the concatenation of both
strings (e.g. MCC = 262 and MNC = 01 results in a HNI of 26201). Combining the HNI with the MSIN (Mobile Subscription
Identification Number) results in the International Mobile Subscriber Identity (IMSI), from which a subscriber can be
further identified. This tool is the Pythonic equivalent of [MCC-MNC](https://www.mcc-mnc.com/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install MCC-MNC requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
> python mcc-mnc.py -cc X/XX # Returns countries matching Country Code (CC)
> python mcc-mnc.py -mcc XXX # Returns countries matching Mobile Country Code (MCC)
> python mcc-mnc.py -mcc XXX -mnc XX/XXX # Returns country matching Mobile Country Code (MCC) and Mobile Network Code (MNC)
> python mcc-mnc.py -cc X/XX -mcc XXX -mnc XX/XXX # Returns country matching Country Code (CC), Mobile Country Code (MCC) and Mobile Network Code (MNC)

# Updating MCC-MNC
> python mcc-mnc.py -update # Downloads and refreshes local CSV and JSON
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/) © Joseph Julian