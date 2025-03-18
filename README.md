# PSX Tracker

Building services to help track an index to guide your investment strategy.

While there are various schools of thoughts around trading, a very safe approach can be to track an index.

However, how do you track an index when you have limited funds that you are injecting at intervals and the mix of shares defining the index and their prices/market cap changes?

The services defined in this repository will help solve this challenge.

The user need to not worry about tracking things. They just input the investments they do.


## Key capabilities to build
- tracking share prices and market capitablization - these are the two main parameters when distrbuting a fund as per an index
- defining an index
- tracking a porfolio of a user (stocks purchased)
- defining how well is the index tracked
- tracking this closeness as prices, index composition, and market capitalization of companies changes
- given funds to invest, what purchasing (given that we can buy whole number shares) improves the index tracking
- if a user wants to sell shares to get a certain amount, what mix of shares will help achieve that amount while improving or minimally imapcting the index tracking


## Architecture and Tools

- FastAPI
- Celery
- BeautifulSoup
- Uvicorn
- SQLAlchemy
- Pydantic
- Redis
- Postgres
- Flyway
- Elasticsearch