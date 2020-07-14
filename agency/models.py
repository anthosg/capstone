# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy


# ----------------------------------------------------------------------------#
# Configuration
# ----------------------------------------------------------------------------#

db = SQLAlchemy()


# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#

# Model for the actors table
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __repr__(self):
        return f"<Actor id='{self.id}' name='{self.name}'>"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# Model for the movies table
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release = db.Column(db.Date)

    def __repr__(self):
        return f"<Movie id='{self.id}' title='{self.title}'>"

    def __init__(self, title, release):
        self.title = title
        self.release = release

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': str(self.release),
        }
