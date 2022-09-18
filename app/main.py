from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from run import db

main = Blueprint("main", __name__)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@main.route("/profile", methods=["POST"])
def profile_post():
    name = request.form.get("book_name")
    books = Books.query.filter_by(title=name)
    if not books:
        flash("Please check you wrote the right name", "error")
        return redirect(url_for("main.profile"))
    return redirect(url_for("main.profile"))