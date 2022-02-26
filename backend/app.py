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
Get movies
"""

@app.route('/movies', methods=['GET'])
def get_movies():
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

"""
Post movies
"""

@app.route('/movies', methods=['POST'])
def create_movie():
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
Get actors
"""

@app.route('/actors', methods=['GET'])
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
Get roles
"""

@app.route('/roles', methods=['GET'])
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
	})

"""
TODO
Get commitments
"""

@app.route('/commitments', methods=['GET'])
def get_commitments():
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

"""
TODO
Get commitments
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