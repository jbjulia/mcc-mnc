"""
A Mobile Country Code (MCC) is used in wireless networks (GSM, CDMA,
UMTS, etc.) to identify the country in which a mobile subscriber (MS)
belongs to. To uniquely identify a mobile subscriber's network provider
the MCC is combined with a Mobile Network Code (MNC). The combination
of MCC and MNC is called the Home Network Identity (HNI), and is the
concatenation of both strings (e.g. MCC = 262 and MNC = 01 results in
a HNI of 26201). Combining the HNI with the MSIN (Mobile Subscription
Identification Number) results in the International Mobile Subscriber
Identity (IMSI), from which a subscriber can be further identified.
This tool is the Pythonic equivalent of https://www.mcc-mnc.com/.
"""

import csv
import json
import os
import sys
import urllib.error
import urllib.request
import uuid


def main(argv):
    """
    Takes passed args and calls respective function. If no valid arg is
    passed, prints list of acceptable args and examples of use.
    :param argv: User's desired arguments
    :return:
    """
    arg_list = [
        "-cc X/XX/XXX:  Returns countries matching Country Code (CC) "
        "(e.g. -cc 93)",
        "-mcc XXX:  Returns countries matching Mobile Country Code (MCC) "
        "(e.g. -mcc 412)",
        "-mcc XXX -mnc XX/XXX:  Returns country matching Mobile Country Code (MCC) and Mobile Network Code (MNC) "
        "(e.g. -mcc 412 -mnc 88)",
        "-cc X/XX/XXX -mcc XXX -mnc XX/XXX:  "
        "Returns country matching Country Code (CC), Mobile Country Code (MCC) and Mobile Network Code (MNC) "
        "(e.g. -cc 93 -mcc 412 -mnc 88)",
        "-update:  Downloads and refreshes local CSV and JSON"
    ]
    try:
        if argv == "-help":
            print("Please refer to the project repository for documentation:  https://github.com/jbjulia/mcc-mnc/")
        if argv[0].lower() == "-update":
            ingest_csv()
        elif argv[0].lower() == "-cc" and len(argv) < 3:
            identify(user_cc=argv[1])  # User's desired CC
        elif argv[0].lower() == "-mcc" and len(argv) < 3:
            identify(user_mcc=argv[1])  # User's desired MCC
        elif argv[0].lower() == "-mcc" and argv[2].lower() == "-mnc":
            identify(user_mcc=argv[1], user_mnc=argv[3])  # User's desired MCC and MNC
        elif argv[0].lower() == "-cc" and argv[2].lower() == "-mcc" and argv[4].lower() == "-mnc":
            identify(user_cc=argv[1], user_mcc=argv[3], user_mnc=argv[5])  # User's desired CC, MCC and MNC
        else:
            print("Error: Invalid arguments.\n\nAcceptable arguments:")
            for item in arg_list:
                print(f"\t{item}")
            print("\nExample:  mcc-mnc.py -cc 93 -mcc 412 -mnc 88")
    except IndexError:
        print("Error: Incorrect argument format.")
        sys.exit(1)


def identify(user_cc=None, user_mcc=None, user_mnc=None):
    """
    Attempts to identify the country of which matches the passed CC
    and/or MCC/MNC. Prints respective MCC-MNC data if match is found.
    :param user_cc: User's desired Country Code (CC)
    :param user_mcc: User's desired Mobile Country Code (MCC)
    :param user_mnc: User's desired Mobile Network Code (MNC)
    :return:
    """
    match_found = False
    match_country = None
    match_list = []
    match_count = 0
    try:
        with open("mcc-mnc.json", "r") as json_file:
            json_data = json.load(json_file)
        if user_cc and not user_mcc and not user_mnc:
            for country in json_data.keys():
                if user_cc == json_data[country]["CC"]:
                    match_found = True
                    match_country = country
                    match_list.append(match_country)
                    match_count += 1
            if match_found:
                print(f"{match_count} Matches Found:  CC [{user_cc}] exists in {match_country.split('-')[0]}.\n")
                for country in json_data.keys():
                    if country in match_list:
                        for key, val in json_data[country].items():
                            print(f"\t{key}: {val}")
                        print("\n")
        elif user_mcc and not user_cc and not user_mnc:
            for country in json_data.keys():
                if user_mcc == json_data[country]["MCC"]:
                    match_found = True
                    match_country = country
                    match_list.append(match_country)
                    match_count += 1
            if match_found:
                print(f"{match_count} Matches Found:  MCC [{user_mcc}] exists in {match_country.split('-')[0]}.\n")
                for country in json_data.keys():
                    if country in match_list:
                        for key, val in json_data[country].items():
                            print(f"\t{key}: {val}")
                        print("\n")
        elif user_mcc and user_mnc and not user_cc:
            for country in json_data.keys():
                if user_mcc == json_data[country]["MCC"] and user_mnc == json_data[country]["MNC"]:
                    match_found = True
                    print(f"Match Found:  MCC [{user_mcc}] and MNC [{user_mnc}] exists in {country.split('-')[0]}, "
                          f"with a Home Network Identity (HNI) of [{user_mcc + user_mnc}].\n")
                    for key, val in json_data[country].items():
                        print(f"\t{key}: {val}")
        elif user_cc and user_mcc and user_mnc:
            for country in json_data.keys():
                if user_cc == json_data[country]["CC"] and \
                        user_mcc == json_data[country]["MCC"] and \
                        user_mnc == json_data[country]["MNC"]:
                    match_found = True
                    print(f"Match Found:  {country.split('-')[0]}.\n")
                    for key, val in json_data[country].items():
                        print(f"\t{key}: {val}")
        if not match_found:
            print("No Match Found.")
    except(IndexError, KeyError, ValueError) as e:
        print(f"Error: The following exception has occurred: {e}")
        sys.exit(1)
    finally:
        print(os.get_terminal_size().columns * "-")
        sys.exit(0)


def ingest_csv():
    """
    Attempts to download CSV from project repository. Checks if CSV
    file exists, removes if true. Creates new CSV and writes data
    decoded from raw URL. Checks if JSON file already exists, removes
    if true. Creates new JSON file and writes empty dictionary. Reads
    in target CSV file containing current MCC-MNC data. Writes data to
    target JSON file and exits after reformatting. Requires network.
    :return:
    """
    try:
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/jbjulia/mcc-mnc/master/src/mcc-mnc/mcc-mnc.csv"
        ) as raw:
            print(f"Decoding raw CSV {'mcc-mnc.csv'}.")
            data = raw.read().decode("utf-8")
        if os.path.exists("mcc-mnc.csv"):
            print(f"Removing old CSV {'mcc-mnc.csv'}.")
            os.remove("mcc-mnc.csv")
        print(f"Creating new CSV {'mcc-mnc.csv'}.")
        f = open("mcc-mnc.csv", "w+")
        print(f"Writing CSV data to {'mcc-mnc.csv'}.")
        f.write(f"{data}")
        print(f"Closing {'mcc-mnc.csv'}.")
        f.close()
        if os.path.exists("mcc-mnc.json"):
            print(f"Removing old JSON {'mcc-mnc.json'}.")
            os.remove("mcc-mnc.json")
        print(f"Creating new JSON {'mcc-mnc.json'}.")
        f = open("mcc-mnc.json", "w+")
        print(f"Writing empty JSON dictionary to {'mcc-mnc.json'}.")
        f.write("{}\r\n")
        print(f"Closing {'mcc-mnc.json'}.")
        f.close()
        with open("mcc-mnc.json", "r") as json_file:
            json_data = json.load(json_file)
        with open("mcc-mnc.csv", "r") as csv_file:
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
        with open("mcc-mnc.json", "w") as out_file:
            json.dump(json_data, out_file, indent=4, sort_keys=True)
            print(f"\nSuccessfully updated JSON file: {os.path.getsize('mcc-mnc.json')} bytes.")
    except OSError as e:
        print(f"Error: Please try again as Administrator: {e}")
        sys.exit(1)
    except urllib.error as e:
        print(f"Error: Unable to resolve URL: {e}")
        sys.exit(1)
    except(IndexError, KeyError, ValueError) as e:
        print(f"Error: The following exception has occurred: {e}")
        sys.exit(1)
    finally:
        print(os.get_terminal_size().columns * "-")
        sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:] if sys.argv[1:] else "-help")
