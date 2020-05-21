from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace later '
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peech.db'
db = SQLAlchemy(app)





class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20),nullable=False,default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
   

    def __repr__(self):
        return 'Pitch' + str(self.id)


pitchs = [
    {
        'author': 'Kyle',
        'title': 'Interview',
        'content': 'Mind your IQ thanks',
        
    },
    {
        'author': 'Daffe',
        'title': 'Life',
        'content': 'Life is cruel',
        
    }
]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pitch',methods=['GET','POST'])
def pitch():
    if request.method == 'POST':
        pitch_title = request.form['title']
        pitch_content = request.form['content']
        pitch_author = request.form['author']
        new_pitch = Pitch(title=pitch_title,content=pitch_content,author=pitch_author)
        db.session.add(new_pitch)
        db.session.commit()
        return redirect('/pitch')
    else:
        pitchs = Pitch.query.order_by(Pitch.date_posted).all()
        
        return render_template('pitch.html',pitchs=pitchs)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/pitch/delete/<int:id>')
def delete(id):
    pitch = Pitch.query.get_or_404(id)
    db.session.delete(pitch)
    db.session.commit()
    return redirect('/pitch')
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('pitch'))
    return render_template('register.html', title='Register', form=form)

@app.route('/pitch/update/<int:id>',methods=['GET','POST'])
def update(id):
    pitchs = Pitch.query.get_or_404(id)
    if request.method == 'POST':
        pitchs.title = request.form['title']
        pitchs.author =  request.form['author']
        pitchs.content = request.form['content']
        db.session.commit()
        return redirect('/pitch')
    else:
        return render_template('update.html',pitchs=pitchs)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'kyle34@outlook.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)