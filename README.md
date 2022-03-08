# Readme



## Pre-requisites
### Python and Postgres
You will need Python3 installed. While this app was originally written with v3.9, it should work with 3.7 and beyond.

You will also need Postgres installed locally. This app was built using v13.2.

### Python Modules and Other Dependencies
Navigate to the /backend folder and create a virtual environment using virtualenv:

```bash
python3 -m venv venv
```

Inside /backend, activate the virtual environment using ```source venv/bin/activate``` and install the dependencies listed in the ```requirements.txt``` file :

```bash
pip install -r requirements.txt
```

## Database
### Database Model
![Casting Agency ERD](https://lucid.app/publicSegments/view/7a26424c-f3d3-4d5c-bd7b-c6a80e2d3521/image.jpeg)

### Create the Database
With Postgres running, create a new database:
```bash
createdb fs-capstone
```

### Creating the Tables
The tables will get set up by launching the app for the first time - see below.

### Sample Data Setup
With Postgres running, you can optionally inject some sample data into the database to get started by using the sample-data.psql file provided. From the backend folder in terminal run:
```bash
psql fs-capstone < database/sample-data.psql
```

## Launch the app

Navigate to the /backend directory in the terminal, ensure the virtual environment is activated and run the below:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

This will launch the app and set up the tables. At this point you can choose to run the sample data setup described in the database section above.

## Testing
From /backend (with Postgres running)

```bash
dropdb fs-capstone_test
createdb fs-capstone_test
psql fs-capstone_test < database/test-sample-data.psql
python test_app.py
```