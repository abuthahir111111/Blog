from flask import Flask, render_template, make_response, jsonify, redirect, flash, url_for, request, abort
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, SignUpForm, AddBlogForm, CommentForm
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from flask_ckeditor import CKEditor
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_gravatar import Gravatar

load_dotenv()
login_manager = LoginManager()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CKEDITOR_PKG_TYPE'] = "standard"
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)
ckeditor = CKEditor(app)
db = SQLAlchemy(app)
login_manager.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    privileges = db.Column(db.Integer, unique=False, nullable=False)
    blog = db.relationship('Blog', back_populates='author')
    comments = db.relationship('Comment', back_populates='author')



class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    author = db.relationship("User", back_populates='blog')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    comment = relationship('Comment', back_populates='blog')



class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    author = db.relationship("User", back_populates='comments')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog = db.relationship('Blog', back_populates='comment')
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    comment_text = db.Column(db.String(300), nullable=False)


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/home")
def home():
    blogs = Blog.query.all()
    return render_template(
        "index.html", 
        user=current_user, 
        blogs=blogs,
    )


@app.route("/about")
def about():
    return render_template("about.html", user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return abort(400)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("User does not exist")
            return redirect(url_for('login'))
    return render_template(
        "login.html", 
        form=form, 
        user=current_user
    )


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email Already exists. Log in")
            return redirect(url_for('login'))
        elif form.password.data != form.confirm_password.data:
            flash("Passwords does not match")
            return redirect(url_for('sign_up'))
        user = User(
            email=form.email.data,
            username=form.name.data,
            password=generate_password_hash(
                password=form.password.data, 
                method="pbkdf2:sha256:10000", 
                salt_length=10
            ),
            privileges=3,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template(
        "sign_up.html", 
        form=form, 
        user=current_user
    )


@app.route("/blog/<int:id>", methods=['GET', 'POST'])
def getblog(id):
    blog_data = Blog.query.get(id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(
                comment_text=comment_form.comment.data,
                author=current_user,
                blog=blog_data,
            )
            db.session.add(comment)
            db.session.commit()
        else:
            return abort(404)
    return render_template(
        "blog.html", 
        blog=blog_data, 
        user=current_user,
        form=comment_form,
    )


@app.route("/blog/add", methods=['GET', 'POST'])
@login_required
def add_blog():
    if current_user.privileges == 3:
        return abort(403)
    form = AddBlogForm()
    if form.validate_on_submit():
        blog = Blog(
            author=current_user,
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=datetime.now().strftime("%B %d, %Y"),
            img_url=form.img_url.data,
            body=form.body.data,
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template(
        "add_blog.html", 
        form=form, 
        user=current_user,
        add_blog=True,
        id=1,
    )


@app.route("/blog/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    if current_user.privileges == 1:
        blog = Blog.query.get(id)
        form = AddBlogForm()

        if form.validate_on_submit():
            blog.title = form.title.data
            blog.subtitle = form.subtitle.data
            blog.img_url = form.img_url.data
            blog.body = form.body.data
            db.session.commit()
            return redirect(url_for('getblog', id=blog.id))
        
        form.title.data = blog.title
        form.subtitle.data = blog.subtitle
        form.img_url.data = blog.img_url
        form.body.data = blog.body
        return render_template(
            "add_blog.html", 
            form=form, 
            user=current_user,
            id=id,
            add_blog=False,
        )
    else:
        return abort(401)


@app.route("/blog/delete/<int:id>")
@login_required
def delete_blog(id):
    if current_user.privileges == 1:
        blog = Blog.query.get(id)
        db.session.delete(blog);
        db.session.commit();
        return redirect(url_for('home'))
    return abort(401)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
