#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from .auth.auth import AuthError, requires_auth
from .config import Config
from .models import db, Actor, Movie


#----------------------------------------------------------------------------#
# Creating app and set routes
#----------------------------------------------------------------------------#

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    db.init_app(app)
    migrate = Migrate(app,db)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )

        return response


    @app.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def read_actors():
        """
        List of actors

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        actors = Actor.query.all()

        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200


    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def create_actor():
        """
        Create actor

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- unprocessable entity
        """

        data = request.get_json()

        if data is None:
            abort(422)

        if 'name' not in data:
            abort(422)
        if 'age' not in data:
            abort(422)
        if 'gender' not in data:
            abort(422)

        actor = Actor(
            name=data['name'],
            age=data['age'],
            gender=data['gender']
        )
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(actor_id):
        """
        Update actor

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        if not actor_id:
            abort(404)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        data = request.get_json()

        if 'name' in data and data['name']:
            actor.name = data['name']

        if 'age' in data and data['age']:
            actor.age = data['age']

        if 'gender' in data and data['gender']:
            actor.gender = data['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format(),
        }), 200


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id):
        """
        Delete actor

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        if not actor_id:
            abort(404)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor_id': actor_id
        }), 200


    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def read_movies():
        """
        List of movies

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        movies = Movie.query.all()

        if not movies:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie():
        """
        Create movie

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- unprocessable entity
        """

        data = request.get_json()

        if data is None:
            abort(422)

        if 'title' not in data:
            abort(422)
        if 'release' not in data:
            abort(422)

        movie = Movie(title=data['title'], release=data['release'])
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(movie_id):
        """
        Update movie

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        if not movie_id:
            abort(404)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        data = request.get_json()

        if 'title' in data and data['title']:
            movie.title = data['title']

        if 'release' in data and data['release']:
            movie.release = data['release']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):
        """
        Delete movie

        Decorators:
            app.route
            requires_auth

        Returns:
            dict -- response with json
            error -- not found
        """

        if not movie_id:
            abort(404)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id
        }), 200


    @app.errorhandler(401)
    def not_authorized(error):
        """
        Unauthorized error

        Decorators:
            app.errorhandler

        Arguments:
            error -- error identifical number

        Returns:
            dict -- response with json
        """

        return jsonify({
            "success": False,
            "error": 401,
            "message": "Authentication error."
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        """
        Forbidden error

        Decorators:
            app.errorhandler

        Arguments:
            error -- error identifical number

        Returns:
            dict -- response with json
        """

        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden."
        }), 403


    @app.errorhandler(404)
    def not_found(error):
        """
        Not found error

        Decorators:
            app.errorhandler

        Arguments:
            error -- error identifical number

        Returns:
            dict -- response with json
        """

        return jsonify({
            "success": False,
            "error": 404,
            "message": "Item not found."
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        """
        Unprocessable entity error

        Decorators:
            app.errorhandler

        Arguments:
            error -- error identifical number

        Returns:
            dict -- response with json
        """

        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request could not be processed."
        }), 422


    @app.errorhandler(AuthError)
    def auth_error(error):
        """
        Auth error

        Decorators:
            app.errorhandler

        Arguments:
            error -- error identifical number

        Returns:
            dict -- response with json
        """

        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code


    return app


if __name__ == '__main__':
    app.run()
