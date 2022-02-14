from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from wtforms import Form, SelectField, TextAreaField, BooleanField, validators, IntegerField
import json
import sys
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


class SubmissionForm(Form):
    seq = TextAreaField('Sequence')
    primer = SelectField('Gene or Primer', choices=[(1, 'GENE'), (2, 'PRIMER')])
    species = SelectField('Species', choices=[(1, 'HUMAN'), (2, 'MOUSE'), (3, 'E.COLI')])


# class Primer():
#     def __init(self, seq, tm, gc):
#         seq = self.seq
#         tm = self.tm
#         gc = self.gc
#
#     def to_dict(self):
#         return {
#             'seq': self.seq,
#             'tm': self.tm,
#             'gc': self.gc
#         }


# @app.route("/")
# def home():
#     l = ['abc', 'def', 'ghi']
#     return render_template("index.html", content="Testing")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seq = db.Column(db.String(), index=True)
    tm = db.Column(db.Integer, index=True)
    gc = db.Column(db.String(256))

    def to_dict(self):
        return {
            'seq': self.seq,
            'tm': self.tm,
            'gc': self.gc
        }


db.create_all()


@app.route("/", methods=['GET', 'POST'])
def submit():
    form = SubmissionForm(request.form)
    if request.method == 'POST':
        s = form.seq.data
        p = form.primer.data
        sp = form.species.data
        primers = findPrimer(s)
        return redirect(url_for('results'))
        # return redirect(url_for('result', seq=s, primer=p, species=sp))
    return render_template("submission.html", form=form)


# def findPrimer(seq):
#     l = len(seq)
#     beg = 0
#     end = 20
#     primers = []
#     while end != l:
#         s = seq[beg:end]
#         param = tm(s)
#         if 65 > param[0] > 55:
#             temp = (s,) + param
#             primers.append(temp)
#         beg += 1
#         end += 1
#     tup = tuple(primers)
#     return tup
# def findPrimer(seq):
#     l = len(seq)
#     beg = 0
#     end = 20
#     primers = dict()
#     primers['data'] = []
#     while end != l:
#         s = seq[beg:end]
#         param = tm(s)
#         if 65 > param[0] > 55:
#             newData = Primer()
#             newData.seq = s
#             newData.tm = param[0]
#             newData.gc = param[1]
#             primers['data'].append(newData.to_dict())
#         beg += 1
#         end += 1
#     return primers

def findPrimer(seq):
    l = len(seq)
    beg = 0
    end = 20
    primers = dict()
    primers['data'] = []
    while end != l:
        s = seq[beg:end]
        param = tm(s)
        if 65 > param[0] > 55:
            newData = Sequence(
                seq=s,
                tm=param[0],
                gc=param[1]
            )
            db.session.add(newData)
        beg += 1
        end += 1
    db.session.commit()
    return primers


def tm(seq):
    seq = seq.upper()
    a = seq.count('A')
    t = seq.count('T')
    g = seq.count('G')
    c = seq.count('C')
    gc = (g + c) / (a + t + g + c) * 100
    gc_content = str(round(gc, 1)) + '%'
    temp = (2 * (a + t)) + (4 * (g + c))
    return temp, gc_content


@app.route('/api/data')
def data():
    return {'data': [i.to_dict() for i in Sequence.query]}

# @app.route("/results/<seq><primer><species>")
# def result(seq, primer, species):
#     if primer == '1':
#         primers = findPrimer(seq)
#     else:
#         t = tm(seq)
#         primers = (seq,) + t
#     return render_template("results.html", content=primers)
# @app.route("/results")
# def results():
#     with open('data.json', 'r') as outfile:
#         _data = json.load(outfile)
#
#     print('-----result-----')
#     print(_data)
#     return render_template("results.html", content=_data)
@app.route("/results")
def results():
    print('-----result-----')
    _data = Sequence.query
    return render_template("results.html", content=_data)


@app.route("/BLAST")
def blast():
    return render_template("blast.html")


if __name__ == "__main__":
    app.run(debug=True)
