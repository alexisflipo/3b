from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import lru_cache
import recommender
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
    name = request.form.get("book_name")
    books = Books.query.filter(Books.title.contains(name)).all()
    print(books)
    return render_template("books.html", books=books)
    # return render_template("books.html", titre=books, url=url,ratings = ratings,description=description)