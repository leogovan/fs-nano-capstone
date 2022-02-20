#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import json
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movie, Actor, RoleType, Role, Commitment

#----------------------------------------------------------------------------#
# Setup
#----------------------------------------------------------------------------#

app = Flask(__name__)
setup_db(app)

CORS(app)

#----------------------------------------------------------------------------#
# Routes
#----------------------------------------------------------------------------#

"""
TODO
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
TODO
Get actors
"""

@app.route('/actors', methods=['GET'])
def get_actors():
	pass

"""
TODO
Get roles
"""

@app.route('/roles', methods=['GET'])
def get_roles():
	pass

"""
TODO
Get commitments
"""

@app.route('/commitments', methods=['GET'])
def get_commitments():
	pass