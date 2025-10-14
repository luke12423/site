from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(50), nullable=False, unique=True)
    password=db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return f'Name : {self.username}'


@app.route('/index')
@app.route('/')
def index():
    profiles=User.query.all()
    return render_template('index.html',profiles=profiles)

@app.route('/registration')
def add_data():
    return render_template('registration.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/catalog')
def card():
    return render_template('catalog.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/add',methods=["POST"])
def profile():
    username=request.form.get("username")
    password=generate_password_hash(request.form.get("password"))
    if username != '' and password != '':
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/registration')

#@app.route('/catalog/<int:id>')
#def card(id):
   # data=Card.query.get(id)

@app.route('/delete/<int:id>')
def erase(id):
    data=User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




