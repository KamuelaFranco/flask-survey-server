from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Server config

app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgres://wwanvaxpkgkakx:GZR1rVHGdyL3t_M8LW_VYQfpHP@ec2-54-83-44-229.compute-1.amazonaws.com:5432/deibu97vueiugu'
except:
    print 'Error connecting to database'

db = SQLAlchemy(app)

# Database models
## Name, Email, Age, About me (block), Address, Gender (male/female)
## Favourite book, Favourite Colours (multiple)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name

# Routes

@app.route('/')
def index():
    return 'Index endpoint'

@app.route('/admin')
def show():
    return 'Admin endpoint for displaying results'

@app.route('/survey')
def create():
    return 'Survey endpoint for POSTing survey'

# Start server

if __name__ == '__main__':
    app.run()
