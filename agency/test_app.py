# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from .app import create_app
from .config import Config
from .models import db, Actor, Movie


# ---------------------------------------------------------
# Tests for app
# ---------------------------------------------------------

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI')


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.init_app(self.app)
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_not_return_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_should_return_all_actors(self):
        actor = Actor(name="Robert De Niro", age="77", gender="male")
        actor.insert()

        res = self.client().get(
            '/actors',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_should_create_new_actor(self):
        new_actor_data = {
            'name': "Jack Nicholson",
            'age': 83,
            'gender': "male"
        }

        res = self.client().post(
            '/actors',
            data=json.dumps(new_actor_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor_data['name'])
        self.assertEqual(data['actor']['age'], new_actor_data['age'])
        self.assertEqual(data['actor']['gender'], new_actor_data['gender'])

        actor_added = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor_added)

    def test_should_update_existing_actor_data(self):
        actor = Actor(name="Denzel Washington", age=100, gender="male")
        actor.insert()

        actor_data_patch = {
            'age': 66
        }

        res = self.client().patch(
            f'/actors/%s' % (actor.id),
            data=json.dumps(actor_data_patch),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'], actor_data_patch['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)

    def test_should_delete_existing_actor(self):
        actor = Actor(name="Humphrey Bogart", age="57", gender="male")
        actor.insert()

        res = self.client().delete(
            f'/actors/%s' % actor.id,
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

    def test_should_not_allow_new_actor_missing_age(self):
        new_actor_data = {
            'name': "Marlon Brando",
            'gender': "male"
        }

        res = self.client().post(
            '/actors',
            data=json.dumps(new_actor_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_should_not_update_existing_actor_if_not_found(self):
        actor_data_patch = {
            'age': '1'
        }

        res = self.client().patch(
            '/actors/1111',
            data=json.dumps(actor_data_patch),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_not_delete_existing_actor_if_not_found(self):
        res = self.client().delete(
            '/actors/1111',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_not_return_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_should_return_all_movies(self):
        # Insert dummy actor into database.
        movie = Movie(title="The Godfather", release="1972-03-24")
        movie.insert()

        res = self.client().get(
            '/movies',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_should_create_new_movie(self):
        new_movie_data = {
            'title': "Casablanca",
            'release': "1973-01-23",
        }

        res = self.client().post(
            '/movies',
            data=json.dumps(new_movie_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], new_movie_data['title'])
        self.assertEqual(data['movie']['release'], new_movie_data['release'])

        movie_added = Movie.query.get(data['movie']['id'])
        self.assertTrue(movie_added)

    def test_should_update_existing_movie_data(self):
        movie = Movie(title="Schindler's List", release="1994-05-01")
        movie.insert()

        movie_data_patch = {
            'release': '1994-05-21'
        }

        res = self.client().patch(
            f'/movies/%s' % (movie.id),
            data=json.dumps(movie_data_patch),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], movie_data_patch['release'])

        movie_updated = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie_updated.id, movie.id)

    def test_should_delete_existing_movie(self):
        movie = Movie(title="Raging Bull", release="1980-12-19")
        movie.insert()

        res = self.client().delete(
            f'/movies/%s' % movie.id,
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], movie.id)

    def test_should_not_allow_new_movie_missing_date(self):
        new_movie_data = {
            'title': "The Shawshank Redemption"
        }

        res = self.client().post(
            '/movies',
            data=json.dumps(new_movie_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_should_not_update_existing_movie_if_not_found(self):
        movie_data_patch = {
            'title': 'WooWoo'
        }

        res = self.client().patch(
            '/movies/1111',
            data=json.dumps(movie_data_patch),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_should_not_delete_existing_movie_if_not_found(self):
        res = self.client().delete(
            '/movies/1111',
            headers={
                'Authorization':
                    f'Bearer {self.app.config.get("PRODUCER_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_assistant_role_should_return_all_actors(self):
        actor = Actor(name="Robert De Niro", age="77", gender="male")
        actor.insert()

        res = self.client().get(
            '/actors',
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("ASSISTANT_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_assistant_role_should_not_create_new_actor(self):
        new_actor_data = {
            'name': "Jack Nicholson",
            'age': 83,
            'gender': "male"
        }

        res = self.client().post(
            '/actors',
            data=json.dumps(new_actor_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("ASSISTANT_ROLE_TOKEN")}'
            }
        )

        self.assertEqual(res.status_code, 401)

    def test_director_role_should_create_new_actor(self):
        new_actor_data = {
            'name': "Jack Nicholson",
            'age': 83,
            'gender': "male"
        }

        res = self.client().post(
            '/actors',
            data=json.dumps(new_actor_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("DIRECTOR_ROLE_TOKEN")}'
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor_data['name'])
        self.assertEqual(data['actor']['age'], new_actor_data['age'])
        self.assertEqual(data['actor']['gender'], new_actor_data['gender'])

        actor_added = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor_added)

    def test_director_role_should_not_create_new_movie(self):
        new_movie_data = {
            'title': "Casablanca",
            'release': "1973-01-23",
        }

        res = self.client().post(
            '/movies',
            data=json.dumps(new_movie_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization':
                    f'Bearer {self.app.config.get("DIRECTOR_ROLE_TOKEN")}'
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
