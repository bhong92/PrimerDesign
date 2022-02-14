from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seq = db.Column(db.String(), index=True)
    tm = db.Column(db.Integer, index=True)
    gc = db.Column(db.String(256))
db.create_all()


# @app.route('/')
# def index():
#     seq = Sequence.query
#     return render_template('results.html', title='Basic Table',
#                            users=seq)


if __name__ == '__main__':
    app.run()