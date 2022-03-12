#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import unittest
import json
import sys
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

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
        self.database_name = "fs-capstone_test"
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

        self.casting_director_token = os.getenv('CASTING_DIRECTOR_TOKEN')
        self.casting_assistant_token = os.getenv('CASTING_ASSISTANT_TOKEN')

        self.test_movie = {
            "movie_name": "Test Movie",
            "genre": "Test Genre",
            "release_date": "2022-02-20",
            "director": "Test Director"
        }

        self.test_actor = {
            "actor_name": "Test Name",
            "phone": "555-55555",
            "age": "37",
            "gender": "F",
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
    def test_retrieve_movies_as_director(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_retrieve_movies_as_assistant(self):
        res = self.client().get('/movies', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    # ##### Create Movies Tests #####
    def test_create_movies(self):
        num_movies_before = len(Movie.query.all())
        res = self.client().post('/movies', json=self.test_movie, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)
        num_movies_after = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(num_movies_after, num_movies_before, 
            "First value is not greater than second value.")
    
    def test_500_create_movies(self):
        res = self.client().post('/movies', json=None, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Internal server error.")

    ##### Update Movies Tests #####
    def test_update_movie(self):
        res = self.client().patch('/movies/2', json={"release_date": "2099-12-31"}, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['patched_movie_id'], 2)
    
    ##### Delete Movie Tests #####
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], 1)
    
    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/10000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request is unprocessable.")


    ##### Retrieve Actors Tests #####
    def test_retrieve_actors_as_director(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    def test_retrieve_actors_as_assistant(self):
        res = self.client().get('/actors', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    ##### Create Actors Tests #####
    def test_create_actors(self):
        num_actors_before = len(Actor.query.all())
        res = self.client().post('/actors', json=self.test_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)
        num_actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(num_actors_after, num_actors_before, 
                "First value is not greater than second value.")

    def test_500_create_actor(self):
        res = self.client().post('/actors', json=None, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Internal server error.")
 
    ##### Delete Actors Tests #####
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], 1)


    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/10000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request is unprocessable.")


    ##### Retrieve Commitments Tests #####
    def test_retrieve_commitments_as_director(self):
        res = self.client().get('/commitments', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['commitments'])
        self.assertTrue(data['total_sommitments'])
    
    def test_retrieve_commitments_as_assistant(self):
        res = self.client().get('/commitments', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['commitments'])
        self.assertTrue(data['total_sommitments'])

    ##### Create Commitments Tests #####
    def test_create_commitments_as_director(self):
        num_commitments_before = len(Commitment.query.all())
        res = self.client().post('/commitments', json=self.test_commitment, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)
        num_commitments_after = len(Commitment.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(num_commitments_after, num_commitments_before, 
            "First value is not greater than second value.")
    
    def test_create_commitments_as_assistant(self):
        num_commitments_before = len(Commitment.query.all())
        res = self.client().post('/commitments', json=self.test_commitment, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)
        num_commitments_after = len(Commitment.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(num_commitments_after, num_commitments_before, 
            "First value is not greater than second value.")
      
    def test_500_create_commitment_as_director(self):
        res = self.client().post('/commitments', json=None, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Internal server error.")

    def test_500_create_commitment_as_assistant(self):
        res = self.client().post('/commitments', json=None, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Internal server error.")

    ##### Delete Commitments Tests #####
    # def test_delete_commitment_as_director(self):
    #     res = self.client().delete('/commitments/2', headers={
    #             "Authorization":
    #             "Bearer {}".format(self.casting_director_token)
    #         })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted_commitment_id'], 2)

    def test_delete_commitment_as_assistant(self):
        res = self.client().delete('/commitments/2', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_commitment_id'], 2)
      
    def test_422_if_commitment_does_not_exist_as_director(self):
        res = self.client().delete('/commitments/10000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request is unprocessable.")
    
    def test_422_if_commitment_does_not_exist_as_assistant(self):
        res = self.client().delete('/commitments/10000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request is unprocessable.")


    ##### Retrieve Roles Tests #####
    def test_retrieve_roles_as_director(self):
        res = self.client().get('/roles', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['roles'])
        self.assertTrue(data['total_roles'])
    
    def test_retrieve_roles_as_assistant(self):
        res = self.client().get('/roles', headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['roles'])
        self.assertTrue(data['total_roles'])


    ##### Create Roles Tests #####
    def test_create_roles(self):
        num_roles_before = len(Role.query.all())
        res = self.client().post('/roles', json=self.test_role, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)
        num_roles_after = len(Role.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(num_roles_after, num_roles_before, 
            "First value is not greater than second value.")
        
    def test_500_create_role(self):
        res = self.client().post('/roles', json=None, headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Internal server error.")
    
    ##### Delete Roles Tests #####
    def test_delete_role(self):
        res = self.client().delete('/roles/4', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_role_id'], 4)
    
    def test_422_if_role_does_not_exist(self):
        res = self.client().delete('/roles/10000', headers={
                "Authorization":
                "Bearer {}".format(self.casting_director_token)
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Request is unprocessable.")

#----------------------------------------------------------------------------#
# Make Tests Executable
#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.main()