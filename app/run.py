from flask import Flask, render_template
from flask_admin import Admin
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
import os
application = Flask(__name__)
application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
user=os.getenv("MYSQL_USER")
user_pwd=os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DATABASE")
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{user_pwd}@mysql_db/{db}"
# application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION')
print(application.config['SQLALCHEMY_DATABASE_URI'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
db = SQLAlchemy(application)
ckeditor = CKEditor(application)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Articles(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    titre = db.Column(db.String(100))
    description = db.Column(db.Text)
    images = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
class PostAdmin(ModelView):
    form_overrides = dict(text=CKEditorField)
    create_template = 'create.html'
    edit_template = 'edit.html'
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),  unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
admin = Admin(application,name='3BackOffice', template_mode='bootstrap3')
# admin.add_view(ModelView(Articles, db.session))
admin.add_view(PostAdmin(Articles, db.session))
admin.add_view(PostAdmin(Users, db.session))
# blueprint for auth routes in our app
from auth import auth as auth_blueprint
application.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
application.register_blueprint(main_blueprint)

@application.route('/')
def index():
    articles = Articles.query.all()
    if current_user.is_authenticated:
        return render_template('articles.html', articles=articles)
    else:
        return render_template('index.html')

@application.route('/<titre>', methods=['GET'])
def articles(titre):
    article = Articles.query.filter_by(titre=titre).first_or_404()
    description = article.description
    return render_template('article.html', titre=article, description=description )

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5090)
    application.run(port=ENVIRONMENT_PORT)