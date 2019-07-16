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
    
    soup = BeautifulSoup(html_doc, 'html.parser')

    fund_name = ''
    if cik in FUNDS.keys():
        fund_name = FUNDS[cik]
    else:
        span_company_name = soup.find('span', {'class': 'companyName'})
        fund_name = span_company_name.contents[0]
    print("CIK matches Fund - %s" % fund_name)

    filing_table = soup.find('table', {'class': 'tableFile2', 'summary': 'Results'})
    # tr_list = filing_table.find_all('tr')[1:]
    # for tr in tr_list:
    #     td_list = list(filter(lambda x: x != '\n', tr.contents))
    #     td_list_contents = list(map(lambda x: x.contents[0], td_list))
    #     print(td_list_contents)
    #     print('\n')

    # Extract the most recent 13F filing.
    # Check if there are atleast 2 table rows. If there are not, this 
    # means that the Fund does not have any Form 13Fs
    all_trs = filing_table.find_all('tr')
    if len(all_trs) < 2:
        raise ValueError("%s has not filed any Form 13Fs" % fund_name)

    top_tr = all_trs[1]
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
