from flask_sqlalchemy import SQLAlchemy

import flask
import flask_cors
import sys

# Server config

app = flask.Flask(__name__)

flask_cors.CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://wwanvaxpkgkakx:GZR1rVHGdyL3t_M8LW_VYQfpHP@ec2-54-83-44-229.compute-1.amazonaws.com:5432/deibu97vueiugu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
## Name, Email, Age, About me (block), Address, Gender (male/female)
## Favourite book, Favourite Colours (multiple)

class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    about_me = db.Column(db.Text)
    address = db.Column(db.Text)
    favourite_book = db.Column(db.String(100))
    favourite_colours = db.Column(db.String(100))
    gender = db.Column(db.Integer)

    def __init__(self, query_params):
        self.name = query_params.get('name', '')
        self.email = query_params.get('email', '')
        self.age = int(query_params.get('age', 0))
        self.about_me = query_params.get('about_me', '')
        self.address = query_params.get('address', '')
        self.gender = int(query_params.get('gender', 0))
        self.favourite_book = query_params.get('favourite_book', '')
        self.favourite_colours = query_params.get('favourite_colours', '')

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
        }

# Routes

@app.route('/')
def index():
    return 'Endpoints: /admin, /survey'

@app.route('/admin')
def show():
    try:
        survey_results = SurveyResult.query.all()
        return flask.json.jsonify(success=True, results=[r.serialise() for r in survey_results])
    except:
        error_message = 'Could not read from database'
        print str(sys.exc_info())
        return flask.json.jsonify(error=error_message)

@app.route('/survey')
def create():
    query_params = flask.request.args.to_dict()
    try:
        survey_result = SurveyResult(query_params=query_params)
        db.session.add(survey_result)
        db.session.commit()
        return flask.json.jsonify(success=True, params=query_params)
    except:
        error_message = 'Could not write to database'
        print str(sys.exc_info())
        return flask.json.jsonify(error=error_message)

# Start server

if __name__ == '__main__':
    app.run()
