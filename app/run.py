from flask import Flask, render_template, abort, session, redirect, request, url_for
from flask_admin import Admin, expose, AdminIndexView
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_login import UserMixin, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import lru_cache
import os
from dotenv import load_dotenv

application = Flask(__name__)
application.config["FLASK_ADMIN_SWATCH"] = "cerulean"
load_dotenv()
user=os.environ.get("MYSQL_USER")
user_pwd=os.environ.get("MYSQL_PASSWORD")
db = os.environ.get("MYSQL_DATABASE")
flask_secret=os.environ.get("FLASK_SECRET_KEY")
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{user_pwd}@mysql_db/{db}"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config.update(
    TESTING=True,
    # SECRET_KEY=flask_secret
    SECRET_KEY='afb8e4199994c69921a67bba559004a4'
)
db = SQLAlchemy(application)

ckeditor = CKEditor(application)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Articles(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    titre = db.Column(db.String(100))
    description = db.Column(db.Text)
    images = db.Column(db.String(100))
    publish_date = db.Column(db.Date)


class PostAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))

    form_overrides = dict(text=CKEditorField)
    create_template = "create.html"
    edit_template = "edit.html"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(100))
    rating = db.Column(db.Float)
    description = db.Column(db.String(10000), default=False)
    language = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    genres = db.Column(db.String(100))
    numRatings = db.Column(db.Float)
    likedPercent = db.Column(db.Float)
    coverImg = db.Column(db.String(10000))
    category = db.Column(db.Integer)
    
# Modify admin view
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("auth.login", next=request.url))

    @expose("/")
    def index(self):
        if not current_user.is_authenticated and current_user.is_admin:
            return redirect(url_for("auth.login"))
        return super(MyAdminIndexView, self).index()


admin = Admin(
    application,
    name="3BackOffice",
    template_mode="bootstrap3",
    index_view=MyAdminIndexView(),
)
admin.add_view(PostAdmin(Articles, db.session))
admin.add_view(PostAdmin(User, db.session))
admin.add_view(PostAdmin(Books, db.session))
admin.add_link(MenuLink(name="Logout", category="", url="/logout"))

# blueprint for auth routes in our app
from auth import auth as auth_blueprint

application.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint

application.register_blueprint(main_blueprint)

@lru_cache(maxsize=1024)
@application.route("/")
def index():
    articles = Articles.query.all()
    if current_user.is_authenticated:
        return render_template("articles.html", articles=articles)
    else:
        return render_template("index.html")


@lru_cache(maxsize=1024)
@application.route("/<titre>", methods=["GET"])
def articles(titre):
    article = Articles.query.filter_by(titre=titre).first_or_404()
    description = article.description
    return render_template("article.html", titre=article, description=description)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5090)
    application.run(port=ENVIRONMENT_PORT)
