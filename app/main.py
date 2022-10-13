from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import lru_cache
from recommender import unserialize_list
main = Blueprint("main", __name__)


@main.route("/predict",  methods=["GET"])
@login_required
def predict():
    books_name = []
    all_books = Books.query.all()
    for i in all_books:
        books_name.append(i.title)
    return render_template("profile.html", name=current_user.name, books_name=books_name)


from run import Books


@main.route("/predict", methods=["POST"])
def predict_post():
    name = request.form.get("book_name")
    books = Books.query.filter_by(Books.title.contains(name)).first_or_404()
    if not books:
        return redirect(url_for("main.predict"))
    return redirect(url_for("main.books"))


@lru_cache(maxsize=1024)
@main.route("/books", methods=["GET", "POST"])
def books():
    try:
        dist = unserialize_list("./distance.sav")
        idlist = unserialize_list("./idlist.sav")
        books = []
        name = request.form.get("book_name")
        try:
            book_id = Books.query.filter(Books.title.contains(name)).first().id
            for newid in idlist[book_id]:
                books.append(Books.query.filter_by(id=newid).first())
            return render_template("books.html", books=books)
        except AttributeError:
            flash("Please check you wrote the right name", "error")
            return redirect(url_for("main.predict"))
    except Exception as e:
        flash("Something went wrong", "error")
        return redirect(url_for("main.predict"))


@lru_cache(maxsize=1024)
@main.route("/books/<id>", methods=["GET"])
def book(id):
    book = Books.query.filter_by(id = id).first()
    return render_template("book.html", book=book)
