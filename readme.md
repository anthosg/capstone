# Full Stack Nanodegree Capstone Project

## Intro

The Casting Agency models a company that is responsible for managing actors and movies.
This is the final project for the Udacity Full Stack Nanodegree.
This project consists of an API with a Python backend and stores data in a Postgresql
database. This project will also incorporate third-party authentication with
Role Based Access Control using Auth0.

## Running the API

API endpoints can be accessed via **https://morning-dusk-09286.herokuapp.com/**
Auth0 information for endpoints that require authentication can be found in `setup.sh`.

## Roles

Casting Assistant:
- Can view actors and movies

Casting Director:
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

Executive Producer:
- All permissions a Casting Director has and...
- Add or delete a movie from the database

## Installing Dependencies

### Python 3.7
Follow instructions to install the correct version of Python for your platform
in the [python docs](https://docs.python.org/3/using/index.html).

### Virtual Environment (venv)
We recommend working within a virtual environment whenever using Python for
projects. This keeps your dependencies for each project separate and organaized.
Instructions for setting up a virual enviornment for your platform can be found
in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
```
python -m venv venv
venv/bin/activate
```

### PIP Dependecies
Once you have your venv setup and running, install dependencies by navigating
 to the root directory and running:
```
 pip install -r requirements.txt
```
This will install all of the required packages included in the `requirements.txt`
file.

### Local Database Setup
Once you create the database, open your terminal, navigate to the root folder, and run:
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
After running, don't forget modify 'SQLALCHEMY\_DATABASE\_URI' variable.

### Local Testing
To test your local installation, run the following command from the root folder:
```
python -m agency.test_app
```
If all tests pass, your local installation is set up correctly.

### Running the server
From within the root directory, first ensure you're working with your created
venv. To run the server, execute the following:
```
export FLASK_APP=agency
export FLASK_DEBUG=true
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and
restart the server automatically.
Setting the `FLASK_APP` variable to `agency` directs Flask to use
the `agency` directory and the `__init__.py` file to find and load the
application.

## Database Schema

Here is a representation of the db schema ([`models.py`](./models.py)):

    actors
    - id (primary key)
    - name
    - age
    - gender

    movies
    - id (primary key)
    - title
    - release

## API Usage

### Error handling

- 401 error handler is returned when there is an issue with the authentication necessary for the action being requested.
```
{
    "error": 401,
    "message": "Authentication error.",
    "success": false
}
```

- 404 error handler occurs when a request resource cannot be found in the database.
```
{
    "error": 404,
    "message": "Item not found.",
    "success": false
}
```

- 422 error handler is returned when the request contains invalid arguments.
```
{
    "error": 422,
    "message": "Request could not be processed.",
    "success": false
}
```

## Endpoints

`GET '/actors'`
`GET '/movies'`
`POST '/actors'`
`POST '/movies'`
`PATCH '/actors/<int:actor_id>'`
`PATCH '/movies/<int:movie_id>'`
`DELETE '/actors/<int:actor_id>'`
`DELETE '/movies/<int:movie_id>'`

GET '/actors'
- Requires authentication (`assistant` role or above).
- Fetches a JSON object with a list of actors in the database.
- Request Arguments: None
- Returns: All actor objects and status code of the request.
```
{
    "actors": [
        {
            "age": 77,
            "gender": "male",
            "id": 1,
            "name": "Robert De Niro"
        },
        {
            "age": "83",
            "gender": "male",
            "id": 2,
            "name": "Jack Nicholson"
        },
    ],
    "success": true
}
```

POST '/actors'
- Requires authentication (`director` role or above).
- Posts a new actor.
- Request Arguments: Name, age, gender.
- Returns: An actor object and status code of the request.
```
{
    "actor": {
        "age": 83,
        "gender": "male",
        "id": 2,
        "name": "Jack Nicholson"
    },
    "success": true
}
```

PATCH '/actors/<int:actor_id>'
- Requires authentication (`director` role or above).
- Patches an existing actor by id in the database.
- Request arguments: Actor ID and JSON object.
For example, to update the age for '/actors/6'
```
{
    "age": 66
}
```
- Returns: An actor object and status code of the request.
```
{
    "actor": {
        "age": 66,
        "gender": "male",
        "id": 4,
        "name": "Denzel Washington"
    },
    "success": true
}
```

DELETE '/actors/<int:actor_id>'
- Requires authentication (`director` role or above).
- Deletes the actor by id from the database.
- Request argument: Actor id.
- Returns: Actor ID and status code of the request.
```
{
    'id': 1,
    'success': true
}
```

GET '/movies'
- Requires authentication (`assistant` role or above).
- Fetches a JSON object with a list of movies in the database.
- Request Arguments: None
- Returns: All movie objects and status code of the request.
```
{
    "movies": [
        {
            "id": 1,
            "release": "1972-03-24",
            "title": "The Godfather"
        },
        {
            "id": 2,
            "release": "1973-01-23",
            "title": "Casablanca"
        },
    ],
    "success": true
}
```

POST '/movies'
- Requires authentication (`producer` role).
- Posts a new movie to the database
- Request Arguments: Title and release.
- Returns: A movie object and status code of the request.
```
{
    "movie": {
        "id": 2,
        "release": "1973-01-23",
        "title": "Casablanca"
    },
    "success": true
}
```

PATCH '/movies/<int:movie_id>'
- Requires authentication (`director` role).
- Patches an existing movie in the database.
- Request arguments: Movie ID and JSON object. For example, to update the release for '/movies/5'
```
{
    "release": "1994-05-21"
}
```
- Returns: A movie object and status code of the request.
```
{
    "movie": {
        "id": 4,
        "release": "1994-05-21",
        "title": "Schindler's List"
    },
    "success": true
}
```

DELETE '/movies/<int:movie_id>'
- Requires authentication (`producer` role).
- Deletes a movie in the database via the DELETE method and using the movie id.
- Request argument: Movie ID
- Returns: Movie ID and status code of the request.
```
{
    'id': 1,
    'success': true
}
```
