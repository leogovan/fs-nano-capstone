#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from crypt import methods
import os
import json
import sys
from flask import Flask, flash, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movie, Actor, RoleType, Role, Commitment, db

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
setup_db(app)

CORS(app)

#----------------------------------------------------------------------------#
# Routes
#----------------------------------------------------------------------------#

"""
Get and Create movies
"""

@app.route('/movies', methods=['GET', 'POST'])
def movies_get_or_post():
	if request.method == 'GET':
		selection = Movie.query.all()
		
		movies = []
		
		for movie in selection:
			movies.append(movie.format())
		
		# Combo of .loads and .dumps strips out the '\' that was occuring for every value
		movies = json.loads(json.dumps(movies))
		
		return jsonify({
			'success': True,
			'movies': movies,
			'total_movies': len(selection)
		})
	
	else:
		body = request.get_json()
	
		new_movie_name = body.get('movie_name')
		new_genre = body.get('genre')
		new_release_date = body.get('release_date')
		new_director = body.get('director')

		movie = Movie(
			movie_name=new_movie_name,
			genre=new_genre,
			release_date=new_release_date,
			director=new_director
		)

		try:
			movie.insert()

			return jsonify({
				'success': True
			}), 200
		
		except:
			movie.undo()
			abort(500)


"""
Delete and Update Movies
"""

@app.route('/movies/<int:movie_id>', methods=['DELETE', 'PATCH'])
def movies_delete_or_patch(movie_id):
	
	movie = Movie.query.get(movie_id)

	if movie is None:
		print("movie is None")
		abort(422)
	
	if request.method == 'DELETE':
		try:
			movie.delete()

			return jsonify({
				'success': True,
				'deleted_movie_id': movie_id
			}), 200
			
		except:
			abort(500)
	
	else:
		try:
			body = request.get_json()
			
			if body is None:
				print("body is None")
				abort(422)
			
			else:
				print("Something is working!")
				release_date_update = body.get('release_date')

				movie.release_date = release_date_update

				movie.update()
				
				return jsonify({
                	"success": True,
					'patched_movie_id': movie_id
            	}), 200
		
		except:
			abort(422)



"""
Get and create actors
"""

@app.route('/actors', methods=['GET', 'POST'])
def actors_get_or_post():
	if request.method == 'GET':
		selection = Actor.query.all()

		actors = []

		for actor in selection:
			actors.append(actor.format())

		# Combo of .loads and .dumps strips out the '\' that was occuring for every value
		actors = json.loads(json.dumps(actors))

		return jsonify({
			'success': True,
			'actors': actors,
			'total_actors': len(selection)
		})
	
	else:
		body = request.get_json()

		new_actor_name = body.get('actor_name')
		new_phone = body.get('phone')
		new_age = body.get('age')
		new_gender = body.get('gender')
		new_image_link = body.get('image_link')

		actor = Actor(
			actor_name=new_actor_name,
			phone=new_phone,
			age=new_age,
			gender=new_gender,
			image_link=new_image_link
		)

		try:
			actor.insert()

			return jsonify({
				'success': True
			}), 200
		
		except:
			actor.undo()
			abort(500)


"""
Delete actor
"""

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
def actors_delete(actor_id):
	actor = Actor.query.get(actor_id)

	if actor is None:
		print("actor is None")
		abort(422)
	
	else:
		try:
			actor.delete()

			return jsonify({
				'success': True,
				'deleted_actor_id': actor_id
			}), 200
			
		except:
			abort(500)


"""
Get and create roles
"""

@app.route('/roles', methods=['GET', 'POST'])
def roles_get_or_post():
	if request.method == 'GET':
		selection = Role.query.all()

		roles = []

		for role in selection:
			roles.append(role.format())

		# Combo of .loads and .dumps strips out the '\' that was occuring for every value
		roles = json.loads(json.dumps(roles))

		return jsonify({
			'success': True,
			'roles': roles,
			'total_roles': len(selection)
		}), 200
	
	else:
		body = request.get_json()

		new_role_number = body.get('role_number')
		new_role_type_id = body.get('role_type_id')
		new_movie_id = body.get('movie_id')

		role = Role(
			role_number=new_role_number,
			role_type_id=new_role_type_id,
			movie_id=new_movie_id
		)

		try:
			role.insert()

			return jsonify({
				'success': True
			}), 200
		
		except:
			role.undo()
			abort(500)


"""
Delete roles
"""
@app.route('/roles/<int:role_id>', methods=['DELETE'])
def roles_delete(role_id):
	role = Role.query.get(role_id)

	if role is None:
		print("role is None")
		abort(422)
	
	else:
		try:
			role.delete()

			return jsonify({
				'success': True,
				'deleted_role_id': role_id
			}), 200
			
		except:
			abort(500)

"""
Get and create commitments
"""

@app.route('/commitments', methods=['GET', 'POST'])
def commitments_get_or_post():
	if request.method == 'GET':
		selection = Commitment.query.all()

		commitments = []

		for commitment in selection:
			commitments.append(commitment.format())

		# Combo of .loads and .dumps strips out the '\' that was occuring for every value
		commitments = json.loads(json.dumps(commitments))

		return jsonify({
			'success': True,
			'roles': commitments,
			'total_roles': len(selection)
		})
	else:
		body = request.get_json()

		new_start_date = body.get('start_date')
		new_end_date = body.get('end_date')
		new_movie_id = body.get('movie_id')
		new_actor_id = body.get('actor_id')
		new_role_type_id = body.get('role_type_id')
		

		commitment = Commitment(
			start_date=new_start_date,
			end_date=new_end_date,
			movie_id=new_movie_id,
			actor_id=new_actor_id,
			role_type_id=new_role_type_id
			
		)

		try:
			commitment.insert()

			return jsonify({
				'success': True
			}), 200
		
		except:
			commitment.undo()
			abort(500)


"""
TODO
Delete commitments
"""
@app.route('/commitments/<int:commitment_id>', methods=['DELETE'])
def commitments_delete(commitment_id):
	commitment = Commitment.query.get(commitment_id)

	if commitment is None:
		print("commitment is None")
		abort(422)
	
	else:
		try:
			commitment.delete()

			return jsonify({
				'success': True,
				'deleted_commitment_id': commitment_id
			}), 200
			
		except:
			abort(500)

"""
Get role-types
"""

@app.route('/role-types', methods=['GET'])
def get_role_types():
	selection = RoleType.query.all()

	role_types = []

	for role_type in selection:
		role_types.append(role_type.format())

	# Combo of .loads and .dumps strips out the '\' that was occuring for every value
	role_types = json.loads(json.dumps(role_types))

	return jsonify({
		'success': True,
		'role_types': role_types,
		'total_role_types': len(selection)
	})