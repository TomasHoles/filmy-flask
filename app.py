from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db = SQLAlchemy(app)

# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    actors = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

# WTForm for adding a new movie
class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    actors = StringField('Actors', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        new_movie = Movie(
            title=form.title.data,
            genre=form.genre.data,
            director=form.director.data,
            actors=form.actors.data,
            rating=form.rating.data
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
