from flask import Flask, redirect, url_for, render_template, request
from wtforms import Form, SelectField, TextAreaField, validators, IntegerField
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key='secretkey'
import requests


class SubmissionForm(Form):
    seq = TextAreaField('Sequence', [validators.InputRequired()])
    primer = SelectField('Gene or Primer', choices=[(1, 'GENE'), (2, 'PRIMER')])
    species = SelectField('Species', choices=[(1, 'HUMAN'), (2, 'MOUSE'), (3, 'E.COLI')])
    bpSize = IntegerField('bpSize', [validators.NumberRange(20, 30)])

class PictureData(Form):
    id = IntegerField()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
Model class to hold primer values
'''
class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seq = db.Column(db.String(), index=True)
    tm = db.Column(db.Integer, index=True)
    gc = db.Column(db.String(256))
    values_A = db.Column(db.Integer, index=True)
    values_T = db.Column(db.Integer, index=True)
    values_G = db.Column(db.Integer, index=True)
    values_C = db.Column(db.Integer, index=True)

    def to_dict(self):
        return {
            'seq': self.seq,
            'tm': self.tm,
            'gc': self.gc,
            'valA': self.values_A,
            'valT': self.values_T,
            'valG': self.values_G,
            'valC': self.values_C
        }


db.create_all()


@app.route("/", methods=['GET', 'POST'])
def submit():
    form = SubmissionForm(request.form)
    if request.method == 'POST':
        db.drop_all()
        db.create_all()
        s = form.seq.data.upper()
        p = form.primer.data
        bpSize = form.bpSize.data
        if p == '1':
            findPrimer(s, bpSize)
        else:
            processPrimer(s)
        return redirect(url_for('results'))
    return render_template("submission.html", form=form)

'''
For gene use, iterates through gene to return array of
potential primers that can be used
'''
def findPrimer(seq, bpSize):
    l = len(seq)
    beg = 0
    end = bpSize
    primers = dict()
    primers['data'] = []
    while end != l:
        s = seq[beg:end]
        param = calculate(s)
        if 65 > param[0] > 55:
            newData = Sequence(
                seq=s,
                tm=param[0],
                gc=param[1],
                values_A=param[2][0],
                values_T=param[2][1],
                values_G=param[2][2],
                values_C=param[2][3],
            )
            db.session.add(newData)
            db.session.commit()
        beg += 1
        end += 1
    return primers

'''
For single primer use, regardless of
values will get added to database
'''
def processPrimer(seq):
    param = calculate(seq)
    newData = Sequence(
                    seq=seq,
                    tm=param[0],
                    gc=param[1],
                    values_A=param[2][0],
                    values_T=param[2][1],
                    values_G=param[2][2],
                    values_C=param[2][3],
                )
    db.session.add(newData)
    db.session.commit()

'''
Takes in a sequence string and returns the
temperature GC content and count of each 
nucleotide
'''
def calculate(seq):
    seq = seq.upper()
    a = seq.count('A')
    t = seq.count('T')
    g = seq.count('G')
    c = seq.count('C')
    gc = (g + c) / (a + t + g + c) * 100
    gc_content = str(round(gc, 1)) + '%'
    temp = (2 * (a + t)) + (4 * (g + c))
    return temp, gc_content, [a, t, g, c]


@app.route('/api/data')
def data():
    return {'data': [i.to_dict() for i in Sequence.query]}



@app.route("/results", methods=['GET', 'POST'])
def results():
    _data = Sequence.query
    form = PictureData(request.form)
    if request.method == 'POST':
        file_name = os.getcwd()
        if os.path.exists('tmp'):
            for f in os.listdir('tmp'):
                if '.png' in f:
                    fn = file_name + '/tmp/' + f
                    os.remove(fn)
        if request.form['id']:
            return getPlot(request.form['id'])




    return render_template("results.html", content=_data)

'''
Sends a POST request to microservice and returns the plot
image generated from data
'''
def getPlot(requestForm):
    primerID = requestForm
    seq = Sequence.query.get(primerID).seq
    A = Sequence.query.get(primerID).values_A
    T = Sequence.query.get(primerID).values_T
    G = Sequence.query.get(primerID).values_G
    C = Sequence.query.get(primerID).values_C

    toPlot = {'title': seq,
              'x_label': 'Nucleotides',
              'y_label': 'Frequency',
              'values': [{'label': 'A', 'value': A},
                         {'label': 'T', 'value': T},
                         {'label': 'G', 'value': G},
                         {'label': 'C', 'value': C}],
              'type': 'bar'}

    url = 'http://127.0.0.1:8000/api/plot'
    url2 = 'http://127.0.0.1:8000/plot'
    requests.post(url, json=toPlot)
    return render_template('index.html', content=url2, seq=seq)


if __name__ == "__main__":
    app.run(debug=True)
