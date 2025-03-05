# DEChallenge

## Setting up the project
### Python
Create a virtual environment running
 
 `python -m venv .venv`
 
  (it's very important you don't name the virtual environment .env) and immediately activate it running
 
 `.venv/Scripts/Activate.ps1`

once done, install poetry running

`pip install poetry`

and

`poetry install`

This should let you have all python dependencies installed.

### Docker
Ensure you have docker and docker-compose installed.

Run

`docker-compose up -d`

Once all containers are running, you need to run 

`alembic upgrade head`

and everything should be ready to go.


## Running the project

Again, make sure all containers are running with

`docker-compose up -d`

and you may start the app with

`fastapi dev .\main.py`

You can now access swagger in localhost:8000/docs

### Api order

So far the ETL process isn't fully automated, so API calls need to be done in order. In sample files you can find a few files to test the system.

First, upload them to **/ingestion/uploadFiles**, then in order run 
- **/digestion/processFiles**
- **/digestion/processLyrics**
- **/digestion/populateTypesense**
- **/digestion/updateGoldLayer**

The query API now should be ready to use.