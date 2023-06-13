import argparse
import sys

from .mccmnc import find_matches, print_matches, update


def get_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="MCC-MNC match and update tool.")
    parser.add_argument("-cc", metavar="CC", type=str, help="Country Code (CC)")
    parser.add_argument(
        "-mcc", metavar="MCC", type=str, help="Mobile Country Code (MCC)"
    )
    parser.add_argument(
        "-mnc", metavar="MNC", type=str, help="Mobile Network Code (MNC)"
    )
    parser.add_argument(
        "-plmn", metavar="PLMN", type=str, help="Public Land Mobile Network (PLMN)"
    )
    parser.add_argument(
        "-update",
        action="store_true",
        help="Downloads and refreshes local CSV and JSON",
    )
    return parser.parse_args()


def main():
    args = get_args()
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
    main()
