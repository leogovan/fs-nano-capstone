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
from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#

def create_app(test_config=None):

	app = Flask(__name__)
	app.config.from_object('config')
	setup_db(app)

	CORS(app)

	@app.after_request
	def after_request(response):
		response.headers.add(
			'Access-Control-Allow-Headers', 
			'Content-Type,Authorization,true')
		response.headers.add(
			'Access-Control-Allow-Methods', 
			'GET,POST,PATCH,DELETE,OPTIONS')
		return response

	#----------------------------------------------------------------------------#
	# Routes
	#----------------------------------------------------------------------------#

	"""
	Get movies
	"""

	@app.route('/movies', methods=['GET'])
	@requires_auth('get:movies')
	def get_movies():
		try:
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
		
		except:
			abort(500)
	
	"""
	Create movie
	"""
	
	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movies')
	def post_movie():
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
	Delete movie
	"""

	@app.route('/movies/<int:movie_id>', methods=['DELETE'])
	@requires_auth('delete:movies')
	def delete_movie(movie_id):
		
		movie = Movie.query.get(movie_id)

		if movie is None:
			print("movie is None")
			abort(422)
		
		try:
			movie.delete()

			return jsonify({
				'success': True,
				'deleted_movie_id': movie_id
			}), 200
				
		except:
			abort(422)


	"""
	Update movie
	"""

	@app.route('/movies/<int:movie_id>', methods=['PATCH'])
	@requires_auth('patch:movies')
	def patch_movie(movie_id):
		
		movie = Movie.query.get(movie_id)

		if movie is None:
			print("movie is None")
			abort(422)
		
		try:
			body = request.get_json()
				
			if body is None:
				print("body is None")
				abort(422)
				
			else:
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
	Get actors
	"""

	@app.route('/actors', methods=['GET'])
	@requires_auth('get:actors')
	def get_actors():
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


	"""
	Create actor
	"""

	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def post_actor():
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
	@requires_auth('delete:actors')
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
	Get roles
	"""

	@app.route('/roles', methods=['GET'])
	@requires_auth('get:roles')
	def get_roles():
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
	
	"""
	Create role
	"""

	@app.route('/roles', methods=['POST'])
	@requires_auth('post:roles')
	def post_role():
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
	Delete role
	"""
	@app.route('/roles/<int:role_id>', methods=['DELETE'])
	@requires_auth('delete:roles')
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
	Get commitments
	"""

	@app.route('/commitments', methods=['GET'])
	@requires_auth('get:commitments')
	def get_commitments():
		selection = Commitment.query.all()

		commitments = []

		for commitment in selection:
			commitments.append(commitment.format())

		# Combo of .loads and .dumps strips out the '\' that was occuring for every value
		commitments = json.loads(json.dumps(commitments))

		return jsonify({
			'success': True,
			'commitments': commitments,
			'total_sommitments': len(selection)
		}), 200

	"""
	Create commitment
	"""

	@app.route('/commitments', methods=['POST'])
	@requires_auth('post:commitments')
	def post_commitment():
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
	Delete commitment
	"""
	@app.route('/commitments/<int:commitment_id>', methods=['DELETE'])
	@requires_auth('delete:commitments')
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
	@requires_auth('get:role-types')
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
	
	#----------------------------------------------------------------------------#
	# Error Handlers
	#----------------------------------------------------------------------------#

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			"success": False, 
			"error": 400,
			"message": "Bad client request."
		}), 400
	
	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({
        	"success": False, 
        	"error": 403,
        	"message": "Access forbidden."
		}), 403
	
	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False, 
			"error": 404,
			"message": "Not found: server cannot find the requested resource."
		}), 404

	@app.errorhandler(405)
	def not_allowed(error):
		return jsonify({
			"success": False, 
			"error": 405,
			"message": "Request method not allowed."
		}), 405
	

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			"success": False, 
			"error": 422,
			"message": "Request is unprocessable."
		}), 422

	@app.errorhandler(500)
	def server_error(error):
		return jsonify({
			"success": False, 
			"error": 500,
			"message": "Internal server error."
		}), 500
	
	@app.errorhandler(AuthError)
	def auth_error(error):
		return jsonify({
			"success": False,
			"error": error.status_code,
			"message": error.error['description']
		}), error.status_code
	
	return app