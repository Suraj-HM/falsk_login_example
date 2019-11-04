
# This is a simple app that demonstrates the flask login extension and a basic authentication interface for future reference

# imports


from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from flask_admin import Admin # this can be used for BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# app


app = Flask(__name__)

app.config['SECRET_KEY'] = 'areallyreallyreallyreallylongsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'secretkeyisnoting'
app.config['FLASK_ADMIN_SWATCH'] = 'paper'


# models

db = SQLAlchemy(app)

class User(UserMixin ,db.Model):
    __tabelname__ = 'user'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(10), unique = True, nullable=False)

    def get_id(self):
        return str(self.user_id).encode(encoding='utf-8').decode('utf-8')

# login


login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# admin


admin = Admin(app, name='login_example', template_mode='bootstrap3')

class MyModelView(ModelView):
    # custom admin view oly alows admin user to access the admin functionalities to edit the models
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(MyModelView(User, db.session))


# forms


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


# routes


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        username = form.name.data
        user = User.query.filter_by(username=username).first()
        if user:
            login_user(user)
            return redirect('/home')
        else:
            flash('User not registred')
    return render_template('home.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    flash(f'user : {current_user} logged in')
    return render_template('home.html', form=None)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    flash('user logged out')
    logout_user()
    return redirect('/')


# run app

if __name__ == "__main__":
    db.create_all()
    app.run(port=3000, debug=True)

