from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

# Server config

app = Flask(__name__)
CORS(app)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgres://wwanvaxpkgkakx:GZR1rVHGdyL3t_M8LW_VYQfpHP@ec2-54-83-44-229.compute-1.amazonaws.com:5432/deibu97vueiugu'
except:
    print 'Error connecting to database'

db = SQLAlchemy(app)

# Database models
## Name, Email, Age, About me (block), Address, Gender (male/female)
## Favourite book, Favourite Colours (multiple)

class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer)
    about_me = db.Column(db.String(500))
    address = db.Column(db.String(250))
    gender = db.Column(db.String(6))
    favourite_book = db.Column(db.String(120))
    favourite_colors = db.Column(db.String(100))

    def __init__(self):
        self.name = name
        self.email = email
        self.age = age
        self.about_me = about_me
        self.address = address
        self.gender = gender
        self.favourite_book = favourite_book
        self.favourite_colors = favourite_colors

    def __repr__(self):
        return '<User %r>' % self.name

# Routes

@app.route('/')
def index():
    return 'Endpoints: /admin, /survey'

@app.route('/admin')
def show():
    try:
        survey_results = SurveyResult.query.all()
        return 'Admin endpoint for displaying results\n', \
            survey_results
    except:
        return 'Error: Could not read from database'

@app.route('/survey')
def create():
    try:
        if request.args.get('name'):
            db.session.add(request.args.get('name'))
        if request.args.get('email'):
            db.session.add(request.args.get('email'))
    except:
        return 'Error: Could not write to database'

    return 'Data saved successfully'

# Start server

if __name__ == '__main__':
    #SQLAlchemy.create_all()
    app.run()
