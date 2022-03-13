# Readme

## Project Motivation
This project is the final demonstration of the skills learned in the Udacity Full-Stack course, featuring the use of:

* Application based on Python 3 and Flask
* Entity modelling using Postgresql
* Creating a number of APIs
* Utilising SQLAlchemy ORM to abstract the application's interaction with the database
* Authentication and RBAC utilising Auth0 as the identity prvoider
* Creating unit tests for the application APIs
* Deploy the application to Heroku

### Project abstract
A casting agency wants to manage the actors on their books and their commitments to filming movies.

The casting assistant can view actors, movies, roles, role-types and commitments. They can also create/delete records for actors to attach or detach them from movies (commitments)

The casting director has the all available privileges

#### Future planned updates
1. An actor can have multiple commitments to multiple films, but the commitment dates must not overlap
2. A movie can have multiple actors starring in it and it can define the maximum number of actors per role, per movie (this is represented by the number of instances of role types associated to a movie)
3. A front end for this

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

test