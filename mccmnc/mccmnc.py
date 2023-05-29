import argparse
import json
import os
import sys
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from tqdm import tqdm

MCC_MNC_URL = "https://www.mcc-mnc.com/"
JSON_PATH = os.path.join(os.path.dirname(__file__), "mccmnc.json")


def get_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='MCC-MNC match and update tool.')
    parser.add_argument('-cc', metavar='CC', type=str, help='Country Code (CC)')
    parser.add_argument('-mcc', metavar='MCC', type=str, help='Mobile Country Code (MCC)')
    parser.add_argument('-mnc', metavar='MNC', type=str, help='Mobile Network Code (MNC)')
    parser.add_argument('-plmn', metavar='PLMN', type=str, help='Public Land Mobile Network (PLMN)')
    parser.add_argument('-update', action='store_true', help='Downloads and refreshes local CSV and JSON')
    return parser.parse_args()


def find_matches(user_cc=None, user_mcc=None, user_mnc=None, user_plmn=None):
    """
    Match the given criteria against the JSON data.

    :param user_cc: User's desired Country Code (CC)
    :param user_mcc: User's desired Mobile Country Code (MCC)
    :param user_mnc: User's desired Mobile Network Code (MNC)
    :param user_plmn: User's desired Public Land Mobile Network (PLMN)
    :return: List of matching PLMNs
    """
    match_list = []

    with open(JSON_PATH, "r") as json_file:
        json_data = json.load(json_file)

    for plmn, details in json_data.items():
        if user_plmn and user_plmn != plmn:
            continue
        if user_cc and str(user_cc) != details["CC"]:
            continue
        if user_mcc and str(user_mcc) != details["MCC"]:
            continue
        if user_mnc and str(user_mnc) != details["MNC"]:
            continue
        match_list.append(plmn)

    return match_list


def print_matches(matches):
    """
    Print the details of the matching PLMNs.

    :param matches: List of matching PLMNs
    """
    with open(JSON_PATH, "r") as json_file:
        json_data = json.load(json_file)

    for match in matches:
        details = json_data[match]
        print(f"\033[1m\033[94mPLMN: {match}\033[0m")
        print(f"  \033[1mMobile Country Code (MCC):\033[0m {details['MCC']}")
        print(f"  \033[1mMobile Network Code (MNC):\033[0m {details['MNC']}")
        print(f"  \033[1mISO:\033[0m {details['ISO']}")
        print(f"  \033[1mCountry:\033[0m {details['COUNTRY']}")
        print(f"  \033[1mCountry Code (CC):\033[0m {details['CC']}")
        print(f"  \033[1mNetwork:\033[0m {details['NETWORK']}")
        print("\n")


def update():
    try:
        with urlopen(MCC_MNC_URL) as raw:
            print(f"Decoding raw HTML from {MCC_MNC_URL}")
            soup = BeautifulSoup(raw, features="html.parser")

        if os.path.exists(JSON_PATH):
            print(f"Removing old JSON dictionary {JSON_PATH}.")
            os.remove(JSON_PATH)

        print(f"Creating new JSON dictionary {JSON_PATH}.")
        json_data = {}
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # Skip the header
        total_rows = len(rows)
        progress_bar = tqdm(total=total_rows, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', colour="blue")

        for i, row in enumerate(rows, start=1):
            cols = row.find_all('td')
            mcc = cols[0].text
            mnc = cols[1].text
            plmn = mcc + mnc  # MCC + MNC
            json_data[plmn] = {
                "MCC": mcc,
                "MNC": mnc,
                "ISO": cols[2].text,
                "COUNTRY": cols[3].text,
                "CC": cols[4].text,
                "NETWORK": cols[5].text.strip() if cols[5].text else "unknown"
            }
            progress_bar.set_description(f"Processing row {i}/{total_rows}")
            progress_bar.update(1)

        progress_bar.close()

        with open(JSON_PATH, "w+") as json_file:
            print(f"\nSaving JSON dictionary to {JSON_PATH}.")
            json.dump(json_data, json_file, indent=4, sort_keys=True)

    except URLError as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)


def main(args):
    """
    Main entry point of the program.

    :param args: Command-line arguments
    """
    try:
        if args.update:
            update()
        else:
            matches = find_matches(args.cc, args.mcc, args.mnc, args.plmn)
            if matches:
                print_matches(matches)
            else:
                print("No match found.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main(get_args())
