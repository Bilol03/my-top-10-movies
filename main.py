from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_project.db"
db.init_app(app)
# CREATE TABLE

class Movies(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year  : Mapped[int] = mapped_column(Integer, nullable=False)
    description : Mapped[str] = mapped_column(String(500), nullable=False)
    rating : Mapped[int] = mapped_column(Float, nullable=False)
    ranking : Mapped[int] = mapped_column(Integer, nullable=False)
    review : Mapped[str] = mapped_column(String(250), nullable=False)
    img_url : Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

class EditForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10 e.g 7.5", validators = [DataRequired()])
    review = StringField(label='Your review' )
    submit = SubmitField(label='Submit')
    
class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')

@app.route("/")
def home():
    movies =     result = db.session.execute(db.select(Movies))
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)

@app.route('/edit', methods=['POST', "GET"])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get("id")
    if request.method == "POST":
        movie_update = db.session.execute(db.select(Movies).where(Movies.id == movie_id) ).scalar()
        movie_update.rating = edit_form.rating.data
        movie_update.review = edit_form.review.data
        db.session.commit()
        return redirect('/')
        
    print(movie_id)
    return render_template('edit.html', edit_form=edit_form)

@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie_delete = db.session.execute(db.select(Movies).where(Movies.id == movie_id) ).scalar()
    db.session.delete(movie_delete)
    db.session.commit()
    return redirect('/')

@app.route('/add')
def add_movie():
    add_form = AddMovieForm()
    
    return render_template('add.html', add_form = add_form)
    
    
if __name__ == '__main__':
    app.run(debug=True)
