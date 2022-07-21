from flask import Flask, render_template
from flask_admin import Admin
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import os
application = Flask(__name__)
application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://remotedbuser:fG$N6PaSpE?f&6zB@178.62.48.158:3306/3b'
# application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@localhost:3306/{os.environ.get('MYSQL_DB')}"
application.config['SQLALCHEMY_DATABASE_URI'] = "mysql://mysql_user:SxEmnfzY94$55eBQ@mysql_db/final_project"
# application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION')
print(application.config['SQLALCHEMY_DATABASE_URI'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
ckeditor = CKEditor(application)
application.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
class Articles(db.Model):
    article_id = db.Column(db.BigInteger, primary_key=True)
    titre = db.Column(db.String(100))
    description = db.Column(db.Text)
    images = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
class PostAdmin(ModelView):
    form_overrides = dict(text=CKEditorField)
    create_template = 'create.html'
    edit_template = 'edit.html'
admin = Admin(application, name='3BackOffice', template_mode='bootstrap3')
# admin.add_view(ModelView(Articles, db.session))
admin.add_view(PostAdmin(Articles, db.session))

@application.route('/')
def index():
    articles = Articles.query.all()
    return render_template('index.html', articles= articles)
@application.route('/articles/<titre>', methods=['GET'])
def articles(titre):
    article = Articles.query.filter_by(titre=titre).first_or_404()
    description = article.description
    return render_template('article.html', titre=article, description=description )

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5090)
    application.run(port=ENVIRONMENT_PORT)