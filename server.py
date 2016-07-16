from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

@app.route('/admin')
def index():
    return 'Admin endpoint for displaying results'

@app.route('/survey')
def create():
    return 'Survey endpoint for POSTing survey'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
