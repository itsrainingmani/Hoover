import requests
from bs4 import BeautifulSoup
from lxml import etree
from hoover import EDGAR, EDGAR_SEARCH, NO_MATCH_CIK, NO_MATCH_TICKER, FUNDS, FORMAT

# Function that returns the Filing information for the most recent Holding Filing
def mostRecentHolding(id):
    validation_url = EDGAR_SEARCH % id
    r = requests.get(validation_url)
    html_doc = r.text

    if NO_MATCH_CIK in html_doc:
        raise ValueError("CIK %s does not exist in EDGAR. Please try again" % id)
    elif NO_MATCH_TICKER in html_doc:
        raise ValueError("Ticker %s does not exist in EDGAR. Please try again" % id)

    soup = BeautifulSoup(html_doc, "html.parser")

    fund_name = ""
    if id in FUNDS.keys():
        fund_name = FUNDS[id]
    else:
        span_company_name = soup.find("span", {"class": "companyName"})
        fund_name = span_company_name.contents[0]
    print("CIK/Ticker matches Fund - %s" % fund_name)

    filing_table = soup.find("table", {"class": "tableFile2", "summary": "Results"})
    # tr_list = filing_table.find_all('tr')[1:]
    # for tr in tr_list:
    #     td_list = list(filter(lambda x: x != '\n', tr.contents))
    #     td_list_contents = list(map(lambda x: x.contents[0], td_list))
    #     print(td_list_contents)
    #     print('\n')

    # Extract the most recent 13F filing.
    # Check if there are atleast 2 table rows. If there are not, this
    # means that the Fund does not have any Form 13Fs
    all_trs = filing_table.find_all("tr")
    if len(all_trs) < 2:
        raise ValueError("%s has not filed any Form 13Fs" % fund_name)

    top_tr = all_trs[1]
    top_result = list(filter(lambda x: x != "\n", top_tr.contents))
    top_result_vals = list(map(lambda x: x.contents[0], top_result))
    return top_result_vals


# Scrape the Filing page table.
# If the 4th Column (Type) in the table has the value INFORMATION TABLE
# and the 3rd Column (Document) ends with .xml, return the URL of the
# XML file
def getInformationTableUrl(url):
    r = requests.get(EDGAR % url)
    soup = BeautifulSoup(r.text, "html.parser")

    xml_infotable_url = ""

    format_file_table = soup.find(
        "table", {"class": "tableFile", "summary": "Document Format Files"}
    )
    tr_list = format_file_table.find_all("tr")[1:]
    for tr in tr_list:
        td_list = list(filter(lambda x: x != "\n", tr.contents))

        if td_list[3].contents[0] == "INFORMATION TABLE":
            doc_link = td_list[2].contents[0]
            if ".xml" in doc_link.contents[0]:
                xml_infotable_url = EDGAR % doc_link["href"]

    return xml_infotable_url


# Given a single Information Table table row (tr), which contains nested values,
# Loop through the element and return a flattened list of values
def processInfoTable(iTable):
    shares = ["" for i in range(12)]
    for vals in iTable:
        tag_name = vals.tag[vals.tag.index("}") + 1 :]
        tag_index = FORMAT[tag_name]
        if len(vals) > 0:
            for v in vals:
                shares[tag_index] = v.text
                tag_index += 1
        else:
            shares[tag_index] = vals.text
    return shares


# Given the url for the xml information table, download the document,
# parse the tree, flatten the rows into a list and return a list of all share values.
def processXml(data_url):
    r = requests.get(data_url)
    infotable_tree = etree.fromstring(bytes(r.text, encoding="utf-8"))
    infotables = list(infotable_tree)
    shares_list = [
        [
            "Issuer",
            "Title of Class",
            "CUSIP",
            "Value",
            "Shr AmT",
            "Shr Type",
            "Put/Call",
            "Investment Discretion",
            "Other Manager",
            "Sole",
            "Shared",
            "None",
        ]
    ]
    for infoTable in infotables:
        shares_list.append(processInfoTable(infoTable))
    return shares_list
