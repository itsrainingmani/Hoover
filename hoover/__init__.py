# init file for Hoover applications

__version__ = "0.1"
SPLASH_TEXT = '''
██╗  ██╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗
██║  ██║██╔═══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗
███████║██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝
██╔══██║██║   ██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
'''

EDGAR = "https://www.sec.gov%s"
EDGAR_SEARCH = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=13F-HR&dateb=&owner=exclude&count=100"
NO_MATCH = "No matching CIK."

FUNDS = {
    '0001166559': 'Gates Foundation',
    '0001352924': 'Caledonia',
    '0001756111': 'Peak6 Investments LLC',
    '0001555283': 'Kemnay Advisory Services Inc.',
    '0001397545': 'HHR Asset Management, LLC',
    '0001543160': 'Benefit Street Partners LLC',
    '0001496147': 'Okumus Fund Management Ltd.',
    '0001357955': 'PROSHARE ADVISORS LLC',
    '0001439289': 'TOSCAFUND ASSET MANAGEMENT LLP',
    '0001086364': 'Black Rock'
}