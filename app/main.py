from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import lru_cache
import recommender
import pickle
main = Blueprint("main", __name__)

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

from run import db, Books

@main.route("/profile", methods=["POST"])
def profile_post():
    name = request.form.get("book_name")
    books = Books.query.filter_by(Books.title.contains(name)).first_or_404()
    if not books:
        flash("Please check you wrote the right name", "error")
        return redirect(url_for("main.profile"))
    return redirect(url_for("main.books"))


@lru_cache(maxsize=1024)
@main.route("/books", methods=['GET', 'POST'])
def books():
    recommender.main()
    with open('./distance.sav', 'rb') as f:
        dist = pickle.load(f)
    with open('./idlist.sav', 'rb') as f:
        idlist = pickle.load(f)
    
    book_list_name = []
    name = request.form.get("book_name")
    book = Books.query.filter(Books.title.contains(name)).first_or_404()
    book_id = book.id
    for newid in idlist[book_id]:
        book_list_name.append(Books.query.filter_by(id=newid).first_or_404())
    books = []
    for name in book_list_name:
        books.append(Books.query.filter(Books.title.contains(name)).first_or_404())
    
    return render_template("books.html", books=books)
    # return render_template("books.html", titre=books, url=url,ratings = ratings,description=description)