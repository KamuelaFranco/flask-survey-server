from flask_sqlalchemy import SQLAlchemy
from uuid import UUID

import flask
import flask_cors
# import ipdb
import json
import os
import sys
import traceback

def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False
    return val.hex == uuid_string.replace('-', '')

# Server config
app = flask.Flask(__name__)
flask_cors.CORS(app)
try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    sys.exit('Error: Provide DATABASE_URL environment key')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
## Name, Email, Age, About me (block), Address, Gender (male/female)
## Favourite book, Favourite Colours (multiple)
class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    about_me = db.Column(db.Text)
    address = db.Column(db.Text)
    favourite_book = db.Column(db.String)
    favourite_colours = db.Column(db.String)
    gender = db.Column(db.Integer)
    uuid = db.Column(db.String(36))
    is_complete = db.Column(db.Boolean)

    def __init__(self, query_params):
        self.name = query_params.get('name', '')
        #print 'name', self.name
        self.email = query_params.get('email' , '')
        self.age = int(query_params.get('age', 0))
        #print self.age
        self.about_me = query_params.get('about_me', '')
        self.address = query_params.get('address', '')
        #print 'address', self.address
        self.gender = int(query_params.get('gender', 0))
        #print 'gender', self.gender
        self.favourite_book = query_params.get('favourite_book', '')
        #print 'fav book', self.favourite_book
        self.favourite_colours = query_params.get('favourite_colours', '')
        #print 'fav colours', self.favourite_colours
        self.uuid = query_params.get('uuid', '')
        #print 'uuid', self.uuid
        self.is_complete = query_params.get('is_complete', False)
        #print 'is_complete', self.is_complete

    def __repr__(self):
        return '<User %r>' % self.name

    def serialise(self):
        return {
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'about_me': self.about_me,
            'address': self.address,
            'gender': self.gender,
            'favourite_book': self.favourite_book,
            'favourite_colors': self.favourite_colours,
            'is_complete': self.is_complete
        }

# Routes

@app.route('/')
def index():
    return flask.json.jsonify(success=True, status='Server running')

@app.route('/admin', methods=['GET'])
def show():
    try:
        survey_results = SurveyResult.query.all()
        return flask.json.jsonify(success=True, results=[r.serialise() for r in survey_results])
    except:
        print str(sys.exc_info())
        return flask.json.jsonify(error='Could not read from database')

@app.route('/survey', methods=['POST'])
def create():
    query_params = flask.request.get_json(force=True)
    uuid = query_params.get('uuid')
    if uuid and validate_uuid4(uuid):
        prev_survey_result = SurveyResult.query.filter_by(uuid=uuid).first()
        if prev_survey_result is None:
            try:
                survey_result = SurveyResult(query_params=query_params)
                db.session.add(survey_result)
                db.session.commit()
                return flask.json.jsonify(success=True, params=query_params)
            except:
                traceback.print_stack()
                print sys.exc_info()
                return flask.json.jsonify(error='Could not write to database')
        if prev_survey_result.is_complete:
            return flask.json.jsonify(error='Survey has already been completed', uuid=uuid)
        if prev_survey_result is not None:
            return flask.json.jsonify(error='Records are updated at this endpoint with PUT')
    return flask.json.jsonify(error='Invalid UUID or UUID not provided')

@app.route('/survey', methods=['PUT'])
def update():
    query_params = flask.request.get_json(force=True)
    uuid = query_params.get('uuid')
    if uuid and validate_uuid4(uuid):
        prev_survey_result = SurveyResult.query.filter_by(uuid=uuid).first()
        if prev_survey_result is None:
            return flask.json.jsonify(error='Requested survey cannot be found', uuid=uuid)
        if prev_survey_result.is_complete:
            return flask.json.jsonify(error='Survey has already been completed', uuid=uuid)
        try:
            SurveyResult.query.filter_by(uuid=uuid).update(query_params)
            db.session.commit()
            return flask.json.jsonify(success=True, params=query_params)
        except:
            print str(sys.exc_info())
            return flask.json.jsonify(error='Could not update record')
    return flask.json.jsonify(error='Invalid UUID or UUID not provided')

# Start server
if __name__ == '__main__':
    app.run()
