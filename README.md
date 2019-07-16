
# Hoover

This Project is the solution to the Plaid Junior Python Engineer coding challenge

# Requirements

This CLI program uses the Requests, BeautifulSoup 4 and lxml python libraries.
You can view the dependencies in the _requirements.txt_ file.

# Usage

For help on how to use this CLI, run the following command:

```shell
$ python -m hoover -h

██╗  ██╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗
██║  ██║██╔═══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗
███████║██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝
██╔══██║██║   ██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝

usage: python -m hoover [-h] CIK [-o | --output file]

Extract EDGAR data for a Fund

positional arguments:
  CIK                   Central Index Key for the Fund

optional arguments:
  -h, --help            show this help message and exit
  -o file, --output file
                        Name of output tsv file
```

From the output of help command, we can see process a Fund's holdings via
```shell
$ python -m hoover CIK
```

where CIK is the Central Index Key of the Fund you want to process.
