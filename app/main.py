from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import lru_cache
from recommender import unserialize_list
import pickle
main = Blueprint("main", __name__)
import logging
@main.route("/predict")
@login_required
def predict():
    return render_template("profile.html", name=current_user.name)

from run import db, Books

@main.route("/predict", methods=["POST"])
def predict_post():
    name = request.form.get("book_name")
    books = Books.query.filter_by(Books.title.contains(name)).first_or_404()
    if not books:
        flash("Please check you wrote the right name", "error")
        return redirect(url_for("main.predict"))
    return redirect(url_for("main.books"))


@lru_cache(maxsize=1024)
@main.route("/books", methods=['GET', 'POST'])
def books():
    dist =  unserialize_list('./distance.sav')
    idlist = unserialize_list('./idlist.sav')
    books = []
    name = request.form.get("book_name")
    book_id = Books.query.filter(Books.title.contains(name)).first().id
    for newid in idlist[book_id]:
        books.append(Books.query.filter_by(id=newid).first())
    
    return render_template("books.html", books=books)