import os
import pprint
import requests
import argparse
from bs4 import BeautifulSoup
from hoover import SPLASH_TEXT, DATA_DIR, __author__
from .utils import nMostRecentHoldings, mostRecentHolding, getInformationTableUrl, processXml


def main(id, output_file_name, add_timestamp, num):
    try:
        # Try to validate the ID
        # holdings = mostRecentHolding(id)
        holdings = nMostRecentHoldings(id, num)
    except ValueError as err:
        print(err)
        return

    if len(holdings) < num:
        print("\nFund doesn't have {} filings".format(num))
    if not os.path.exists(DATA_DIR):
        print("Creating directory to hold file outputs\n")
        os.mkdir(DATA_DIR)

    for i, holding in enumerate(holdings):
        # Get the href value for 'Documents' link in table
        document_url = holding[1]["href"]

        # Get the URL for Form 13F Information Table
        infotable_url = getInformationTableUrl(document_url)

        # Download the Form 13F info table, parse the XML and
        # return a list of share and information
        list_of_shares = processXml(infotable_url)

        print("\nWriting Holding {} to Tab Separated File".format(i+1))
        new_file_name = DATA_DIR + output_file_name + "-" + id + "-" + str(i)

        # If the -t or --time flags were present during invocation
        # Get current timestamp formatted into a string and append
        # it to the end of the output filename
        if add_timestamp:
            print("(with timestamp)\n")
            from datetime import datetime

            time_stamp = datetime.now()
            new_file_name += "-" + time_stamp.strftime("%Y%m%d_%H-%M-%S")

        new_file_name += ".tsv"

        with open(new_file_name, "w+") as out_file:
            for sh in list_of_shares:
                out_file.write("\t".join(sh) + "\n")

    print("Done!")
    return


if __name__ == "__main__":
    print(SPLASH_TEXT + "By %s\n" % __author__)

    # Construct the ArgumentParser
    parser = argparse.ArgumentParser(
        description="Extract EDGAR data for a Fund",
        usage="python -m hoover [-h] ID [-o | --output file] [-t | --time] [-n | --num]",
    )
    parser.add_argument("ID", type=str, help="CIK or Ticker for a Fund")
    parser.add_argument(
        "-o",
        "--output",
        help="Name of output tsv file",
        metavar="file",
        default="Form13F",
    )
    parser.add_argument(
        "-t",
        "--time",
        dest="timestamp",
        action="store_true",
        help="Flag to add timestamp to the output file name",
    )
    parser.add_argument(
        "-n",
        "--num",
        help="Flag to add timestamp to the output file name",
        metavar="num",
        default=1
    )
    parser.set_defaults(timestamp=False)
    args = parser.parse_args()

    try:
        id = int(args.ID)
        print("CIK to process - %s" % id)
    except:
        print("Ticker to process - %s" % args.ID)

    num = int(args.num)

    if num < 1:
        num = 1
    main(args.ID, args.output, args.timestamp, num)
