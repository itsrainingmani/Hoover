import requests
from bs4 import BeautifulSoup
from lxml import etree
from hoover import EDGAR, EDGAR_SEARCH, NO_MATCH, FUNDS

# Function that returns the Filing information for the most recent Holding Filing
def mostRecentHolding(cik):
    cik_validate_url = EDGAR_SEARCH % cik
    r = requests.get(cik_validate_url)
    html_doc = r.text

    if NO_MATCH in html_doc:
        raise ValueError("CIK %s does not exist in EDGAR. Please try again" % cik)

    if cik in FUNDS.keys():
        print("CIK matches Fund - %s \n" % FUNDS[cik])
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    filing_table = soup.find('table', {'class': 'tableFile2', 'summary': 'Results'})
    # tr_list = filing_table.find_all('tr')[1:]
    # for tr in tr_list:
    #     td_list = list(filter(lambda x: x != '\n', tr.contents))
    #     td_list_contents = list(map(lambda x: x.contents[0], td_list))
    #     print(td_list_contents)
    #     print('\n')

    # Extract the most recent 13F filing
    all_trs = filing_table.find_all('tr')
    if len(all_trs) == 0:
        raise ValueError("CIK does not have any Form 13Fs")

    top_tr = filing_table.find_all('tr')[1]
    top_result = list(filter(lambda x: x != '\n', top_tr.contents))
    top_result_vals = list(map(lambda x: x.contents[0], top_result))
    return top_result_vals

def getInformationTableUrl(url):
    r = requests.get(EDGAR % url)
    soup = BeautifulSoup(r.text, 'html.parser')

    xml_infotable_url = ''

    format_file_table = soup.find('table', {'class': 'tableFile', 'summary': 'Document Format Files'})
    tr_list = format_file_table.find_all('tr')[1:]
    for tr in tr_list:
        td_list = list(filter(lambda x: x != '\n', tr.contents))
        
        if td_list[3].contents[0] == 'INFORMATION TABLE':
            doc_link = td_list[2].contents[0]
            if ".xml" in doc_link.contents[0]:
                xml_infotable_url = EDGAR % doc_link['href']

    return xml_infotable_url

def processInfoTable(iTable):
    shares = []
    for vals in iTable:
        if len(vals) > 0:
            for v in vals:
                shares.append(v.text)
        else:
            shares.append(vals.text)
    return shares

def processXml(data_url):
    r = requests.get(data_url)
    infotable_tree = etree.fromstring(bytes(r.text, encoding='utf-8'))
    infotables = list(infotable_tree)
    shares_list = [['Issuer', 'Title of Class', 'CUSIP', 'Value', 'SHRS OR PRN AMT', 'SH/PRN', 'Investment Discretion', 'Voting Authority - Sole', 'Voting Authority - Shared', 'Voting Authority - None']]
    for infoTable in infotables:
        shares_list.append(processInfoTable(infoTable))
    return shares_list
