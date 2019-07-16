import requests
import argparse
from bs4 import BeautifulSoup
from hoover import SPLASH_TEXT
from .utils import mostRecentHolding, getInformationTable

def main(cik):
    try:
        # Try to validate the CIK
        holdings = mostRecentHolding(cik)
        print(holdings)
    except ValueError as err:
        print(err)
        return

    document_url = holdings[1]['href']
    data = getInformationTable(document_url)
    print(data)


if __name__ == '__main__':
    print(SPLASH_TEXT)

    parser = argparse.ArgumentParser(description='Extract EDGAR data for a Fund', usage='python -m hoover [-h] CIK [-o | --output file]')
    parser.add_argument('CIK', type=str, help='Central Index Key for the Fund')
    parser.add_argument('-o', '--output', help='Name of output tsv file', metavar='file')

    args = parser.parse_args()

    try:
        cik = int(args.CIK)
        print("CIK to process - %s" % cik)
    except:
        print("The CIK has to be a valid number")
        exit(-1)

    main(args.CIK)