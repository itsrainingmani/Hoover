
# Hoover

This Project is the solution to the Plaid Junior Python Engineer coding challenge

# Requirements

This CLI program uses the Requests, BeautifulSoup 4 and lxml python libraries.
You can view the dependencies in the _requirements.txt_ file.

Install the packages from the _requirements.txt_ using:

```shell
pip install -r requirements.txt
```

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

usage: python -m hoover [-h] ID [-o | --output file] [-t | --time]

Extract EDGAR data for a Fund

positional arguments:
  ID                    CIK or Ticker for a Fund

optional arguments:
  -h, --help            show this help message and exit
  -o file, --output file
                        Name of output tsv file
  -t, --time            Flag to add timestamp to the output file name
```

## Examples

To generate the _.tsv_ file for the Bill & Melinda Gates Foundation (CIK - 0001166559), we run following command:

```shell
$ python -m hoover 0001166559


██╗  ██╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗
██║  ██║██╔═══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗
███████║██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝
██╔══██║██║   ██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝

CIK to process - 1166559
CIK\Ticker matches Fund - Gates Foundation
Creating directory to hold file output

Writing Holding Info to Tab Separated File

Done!
```

When you run the CLI for the first time, the program will automatically create a _forms_ directory to hold the outputs of the CLI. On future runs of the CLI, it will detect the presence of the _forms_ directory and use it.

### Timestamp

The default _.tsv_ file name format is: __Form13F-CIK.tsv__. If you add the _-t_ or _--time_ flag when invoking the CLI, the program will automatically add a timestamp to the end of the filename.

For example:

```shell
python -m hoover 0001166559 -t
```

will create a file named:

```text
Form13F-0001166559-20190716_11-34-09.tsv
```

### Custom Filename

You can also specify a custom name for the output file, by using the _-o_ or _--output_ arguments.

```shell
python -m hoover 0001166559 -o billmelindagates
```

will create a file named:

```text
billmelindagates-0001166559.tsv
```

# Performance

Of the 10 Funds given in the coding challenge prompt, Black Rock (CIK - 0001086364) had the largest number of rows in their most recent holding, clocking in at 4511 rows.

I wanted to measure the time it took for the Hoover CLI to request, parse and generate the _.tsv_ file for Black Rock.

The output of running this command is (for a single execution):

```shell
time python -m hoover 0001086364

real  0m2.538s
user  0m0.000s
sys   0m0.031s
```
