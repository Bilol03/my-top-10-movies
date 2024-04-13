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
    title : Mapped[str] = mapped_column(String(250), unique=True)
    year  : Mapped[int] = mapped_column(Integer)
    description : Mapped[str] = mapped_column(String(500))
    rating : Mapped[int] = mapped_column(Float)
    ranking : Mapped[int] = mapped_column(Integer)
    review : Mapped[str] = mapped_column(String(250))
    img_url : Mapped[str] = mapped_column(String(250))

with app.app_context():
    db.create_all()

class EditForm(FlaskForm):
    rating = FloatField(label="Your rating out of 10 e.g 7.5", validators = [DataRequired()])
    review = StringField(label='Your review' )
    submit = SubmitField(label='Submit')
    
class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')



MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjgxZWMyYzQzODIwZWZlMDlhZDgxZmEwM2JjMmVlYiIsInN1YiI6IjY2MThjNjg0NmYzMWFmMDE0OTlhNWU0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eJg4Kab1x0ynsUpteIZ1mxAclWc9rUWG1defHDL-5ts"
    }

@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movies).order_by(Movies.rating))
    ranked = all_movies.scalars().all()
    
    print(ranked)
    for i in range(len(ranked)):
        ranked[i].ranking = len(ranked) - i
    db.session.commit()
    return render_template("index.html", movies=ranked)

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

@app.route('/add', methods=['POST', 'GET'])
def movie_add():
    add_form = AddMovieForm()

    
    if request.method == 'POST':
        title = add_form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page=1"

        response = requests.get(url, headers=headers)
        response = response.json()
        print(response)
        return render_template('select.html', movies=response)

    return render_template('add.html', add_form = add_form)
   
@app.route('/add_movie') 
def add_movie():
    id = request.args.get('id')
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    response = requests.get(url=url, headers=headers)
    response = response.json()
    new_movie = Movies(
        id = id,
        title = response['title'],
        year = response['release_date'],
        description = response['overview'],
        rating = 0,
        ranking = response['popularity'],
        review = "None",
        img_url = f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True, port=3000)
