from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
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
print("**done!!!")

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
