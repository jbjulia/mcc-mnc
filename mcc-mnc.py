"""
A Mobile Country Code (MCC) is used in wireless networks (GSM, CDMA,
UMTS, etc.) to identify the country in which a mobile subscriber (MS)
belongs to. To uniquely identify a mobile subscriber's network provider
the MCC is combined with a Mobile Network Code (MNC). The combination
of MCC and MNC is called the Home Network Identity (HNI), and is the
concatenation of both strings (e.g. MCC = 262 and MNC = 01 results in
an HNI of 26201). Combining the HNI with the MSIN (Mobile Subscription
Identification Number) results in the International Mobile Subscriber
Identity (IMSI), from which a subscriber can be further identified.
"""

import csv
import json
import sys
import uuid


def main(argv):
    """
    Takes passed arg(s) and calls respective function. If no valid arg
    is passed, displays list of acceptable args and example of use.
    :param argv:
    :return:
    """
    arg_list = [
        # "-cc:  Country Code"
        "-mcc:  Mobile Country Code",
        "-mnc:  Mobile Network Code"
    ]
    try:
        if argv == "-help":
            print("Please refer to to project repository for documentation:  https://github.com/jbjulia/mcc-mnc/")
        elif argv[0].lower() == "-mcc" and not argv[2]:
            identify(argv[1])
        elif argv[0].lower() == "-mcc" and argv[2].lower() == "-mnc":
            identify(argv[1].lower(), argv[3].lower())
        else:
            print("Argument not recognized.\n\nAcceptable arguments:")
            for item in arg_list:
                print(f"\t{item}")
            print("\nExample 1:  mcc-mnc.py -mcc 544 -mnc 11")
    except IndexError:
        print("Incorrect argument format.")
        sys.exit(1)


def identify(user_mcc, user_mnc=None):
    """
    Attempts to identify the country of which matches the passed MCC
    and MNC. Prints respective MCC-MNC data if match is found.
    :param user_mcc:
    :param user_mnc:
    :return:
    """
    match_found = False
    try:
        with open("data/mcc-mnc.json", "r") as json_file:
            json_data = json.load(json_file)
        if not user_mnc:
            for country in json_data.keys():
                if user_mcc in json_data[country]["MCC"]:
                    match_found = True
                    print(f"Match found:  MCC [{user_mcc}] exists in {country}")
        else:
            for country in json_data.keys():
                if user_mcc in json_data[country]["MCC"] and user_mnc in json_data[country]["MNC"]:
                    match_found = True
                    print(f"Match found:  MCC [{user_mcc}] and MNC [{user_mnc}] exists in {country.split('-')[0]}\n")
                    for key, val in json_data[country].items():
                        print(f"{key}: {val}")
        if not match_found:
            print("No match found.")
    except(IndexError, KeyError, ValueError) as e:
        print(e)
        sys.exit(1)


def ingest_csv():
    """
    Reads in target CSV file containing current MCC-MNC data. Writes
    data to target JSON file and exits after reformatting.
    :return:
    """
    try:
        with open("data/mcc-mnc.json", "r") as json_file:
            json_data = json.load(json_file)
        with open("data/mcc-mnc.csv", "r") as csv_file:
            for line in csv.reader(csv_file):
                if line[3] in json_data.keys():
                    json_data.update(
                        {
                            f"{line[3]}-{str(uuid.uuid4())}": {
                                "MCC": line[0],
                                "MNC": line[1],
                                "ISO": line[2],
                                "CC": line[4],
                                "NETWORK": line[5] if line[5] else "unknown"
                            }
                        }
                    )
                else:
                    json_data.update(
                        {
                            line[3]: {
                                "MCC": line[0],
                                "MNC": line[1],
                                "ISO": line[2],
                                "CC": line[4],
                                "NETWORK": line[5] if line[5] else "unknown"
                            }
                        }
                    )
        with open("data/mcc-mnc.json", "w") as out_file:
            json.dump(json_data, out_file, indent=4, sort_keys=True)
    except(IndexError, KeyError, ValueError) as e:
        print(e)
        sys.exit(1)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    # ingest_csv()  # Un-hash to refresh 'mcc-mnc.json' file
    main(sys.argv[1:] if sys.argv[1:] else "-help")
