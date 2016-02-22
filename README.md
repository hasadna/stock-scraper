

A collection of commands allowing extraction of Israeli stock market data.
The data is scraped from the http://maya.tase.co.il/bursa website.

In order to run the commands you need to setup the db and tool.

Data scraped:

1. Company data - name, email, website, phone, etc.
2. Market cap per company - market value
3. Stakeholder data per company - security name, stock count, capital rate, etc.
4. Management data per company - position, stock count, capital rate, etc.
5. Financial report per company - balance, assets, equity, etc.

## Setup

### Install tool
1. Clone the project and enter it's root directory.
2. `$ pip install -r requirements.txt`.

### Prepare DB
The database will keep the scraped data.

1. Create a db and update `bursa/settings.py` accordingly. For example:

	```
	DATABASE = {
     'class': 'MySQLDatabase',
	  'name': 'bursa',
	  'host': '',
	  'user': 'root',
	  'password': ''
	}
	```
2. Create the tables by running `$ python manage.py`

### Choosing a browser for the scraper
Since scrapers use web browsers, a browser should be made available on the machine running the scrape commands.
Currently, the scraper is hardcoded to use Firefox so make sure it's installed either as the standard version or headless.

## Running scrape commands
Basically, each type of company data has it's own scraper. Some data is static (e.g. company name) and some is time based (e.g market cap).

Here are the available commands:

* `python scrape.py info` - extracts all companies and they're static information. Companies already in the db are ignored.
* `python scrape.py market_cap` - extracts market cap data for each company in the db.
* `python scrape.py stakeholder` - extracts stakeholder data for each company in the db.
* `python scrape.py management` - extracts management data for each company in the db.
* `python scrape.py financial_report` - extracts financial report data for each company in the db.