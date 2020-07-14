import os
from dotenv import load_dotenv

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

    # Database variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_TEST_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    # Auth0 variables
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_ALGORITHMS = os.environ.get('AUTH0_ALGORITHMS', ['RS256'])

    # Tokens
    ASSISTANT_ROLE_TOKEN = os.environ.get('ASSISTANT_ROLE_TOKEN')
    DIRECTOR_ROLE_TOKEN = os.environ.get('DIRECTOR_ROLE_TOKEN')
    PRODUCER_ROLE_TOKEN = os.environ.get('PRODUCER_ROLE_TOKEN')
