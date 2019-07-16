import os
import pprint
import requests
import argparse
from bs4 import BeautifulSoup
from hoover import SPLASH_TEXT
from .utils import mostRecentHolding, getInformationTableUrl, processXml

DATA_DIR = 'forms/'

def main(cik, output_file_name, add_timestamp):
    try:
        # Try to validate the CIK
        holdings = mostRecentHolding(cik)
    except ValueError as err:
        print(err)
        return

    # Get the href value for 'Documents' link in table
    document_url = holdings[1]['href']

    # Get the URL for Form 13F Information Table
    infotable_url = getInformationTableUrl(document_url)

    # Download the Form 13F info table, parse the XML and
    # return a list of share and information
    list_of_shares = processXml(infotable_url)

    if not os.path.exists(DATA_DIR):
        print("Creating directory to hold file outputs\n")
        os.mkdir(DATA_DIR)

    print("Writing Holding Info to Tab Separated File\n")
    new_file_name = DATA_DIR + output_file_name + '-' + cik

    if add_timestamp:
        from datetime import datetime
        time_stamp = datetime.now()
        new_file_name += '-' + time_stamp.strftime('%Y%m%d_%H-%M-%S')
    
    new_file_name += '.tsv'

    with open(new_file_name, 'w+') as out_file:
        for sh in list_of_shares:
            out_file.write('\t'.join(sh) + '\n')
    print("Done!")
    return

if __name__ == '__main__':
    print(SPLASH_TEXT)

    parser = argparse.ArgumentParser(description='Extract EDGAR data for a Fund', usage='python -m hoover [-h] CIK [-o | --output file] [-t | --time]')
    parser.add_argument('CIK', type=str, help='Central Index Key for the Fund')
    parser.add_argument('-o', '--output', help='Name of output tsv file', metavar='file', default='Form13F')
    parser.add_argument('-t', '--time', dest='timestamp', action='store_true', help='Flag to add timestamp to the output file name')
    parser.set_defaults(timestamp=False)
    args = parser.parse_args()

    try:
        cik = int(args.CIK)
        print("CIK to process - %s" % cik)
    except:
        print("The CIK has to be a valid number")
        exit(-1)

    main(args.CIK, args.output, args.timestamp)