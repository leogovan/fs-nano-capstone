#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import unittest
import json
import sys
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, Commitment, Role, RoleType

#----------------------------------------------------------------------------#
# Unit Test Cases
#----------------------------------------------------------------------------#

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Actor test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #----------------------------------------------------------------------------#
        # Test Data
        #----------------------------------------------------------------------------#

        self.test_movie = {
            "movie_name": "Test Movie",
            "genre": "Test Genre",
            "release_date": "2022-02-20",
            "director": "Test Director"
        }

        self.test_actor = {
            "actor_name": "Test Name",
            "phone": "Test Phone",
            "age": "Test Age",
            "gender": "Test Gender",
            "image_link": "www.test-domain.com/media/some-image-url.jpg"
        }

        self.test_commitment = {
            "start_date": "2022-02-20",
            "end_date": "2022-02-21",
            "movie_id": "1",
            "actor_id": "1",
            "role_type_id": "1"
        }

        self.test_role = {
            "role_number": "1",
            "movie_id": "1",
            "role_type_id": "1"
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    #----------------------------------------------------------------------------#
    # Tests
    #----------------------------------------------------------------------------#

    ##### Retrieve Movies Tests #####
    def test_retrieve_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    ##### Create Movies Tests #####
    def test_create_movies(self):
        num_questions_before = len(Movie.query.all())
        res = self.client().post('movies')
        data = json.loads(res.data)


    
    ##### Delete Movies Tests #####

    ##### Update Movies Tests #####
    
    ##### Retrieve Actors Tests #####
    def test_retrieve_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    ##### Create Actors Tests #####


    ##### Delete Actors Tests #####


    ##### Retrieve Commitments Tests #####

    ##### Create Commitments Tests #####
    
    ##### Delete Commitments Tests #####

    ##### Retrieve Roles Tests #####

    ##### Create Roles Tests #####
    
    ##### Delete Roles Tests #####




#----------------------------------------------------------------------------#
# Make Tests Executable
#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.main()