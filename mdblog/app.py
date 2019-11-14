from flask import Flask
from flask import render_template  # vid 204, 0:55
from flask import request          # vid 206, 2:50 
from flask import redirect         # vid 206, 5:32 
from flask import url_for          # vid 206, 6:19
from flask import session          # vid 206, 6:30
from flask import g                # vid 207, 5:05
from flask import flash            # vid 208, 3:30

import sqlite3
import os


flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")  # vid 208, 7:45

if "MDBLOG_CONFIG" in os.environ:      # video 208, 7:00
    flask_app.config.from_envvar("MDBLOG_CONFIG")

@flask_app.route("/")
def view_welcome_page():
    return render_template("welcome_page.jinja")

@flask_app.route("/about/")
def view_about():
    return render_template("about.jinja")

@flask_app.route("/admin/")
def view_admin():
    if "logged" not in session:
        flash("You must be logged in", "alert-danger")
        return redirect(url_for("view_login"))
    return render_template("admin.jinja")

@flask_app.route("/articles/", methods=["GET"])
def view_articles():
    db = get_db()    # vysvetlenie zac video 208
    cur = db.execute("select * from articles order by id desc")
    articles = cur.fetchall()
    return render_template("articles.jinja", articles=articles)

@flask_app.route("/articles/", methods=["POST"])        # vid 208, 3:00
def add_article():
    db = get_db()     
    db.execute("insert into articles (title, content) values (?, ?)",
            [request.form.get("title"), request.form.get("content")])
    db.commit()
    flash("Article was saved", "alert-success")
    return redirect(url_for("view_articles"))

@flask_app.route("/articles/<int:art_id>/")
def view_article(art_id):
    db = get_db()   # vysvetl. video 208 , 1:00
    cur = db.execute("select * from articles where id=(?)",[art_id])
    article = cur.fetchone()
    if article:
        return render_template("article.jinja", article=article)
    return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route("/login/", methods=["GET"])   # vid 206 , 4:23
def view_login():
    return render_template("login.jinja")

@flask_app.route("/login/", methods=["POST"]) # vid 206 , 4:23
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    if username == flask_app.config["USERNAME"] and \
            password == flask_app.config["PASSWORD"]:    # vid 208 , 8:25
        session["logged"] = True
        flash("Login succesful", "alert-success")
        return redirect(url_for("view_admin"))
    else:
        flash("invalid credentials", "alert-danger")
        return redirect(url_for("view_login"))

@flask_app.route("/logout/", methods=["POST"])   # vid 206, 10:10
def logout_user():
    session.pop("logged")
    flash("logout succesfull", "alert-success")
    return redirect(url_for("view_welcome_page"))


## UTILS
# funkcia, ktorou sa pripojim na databazu, video 207, 3:40
def connect_db():
    rv = sqlite3.connect(flask_app.config["DATABASE"])    # 208, 8:50
    rv.row_factory = sqlite3.Row   # vysvetleny riadok 207 , 4:33
    return rv

# funkcia na spojenie s databazou, video 207, 5:00 
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# funkcia na zatvorenie databazy, video 207, 7:00
@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

# funkcia, inicializacia databazy pomocou flask (budeme viac pouzivat)
# video 207, od 8:40
def init_db(app):
    with app.app_context():
        db = get_db()
        with open("mdblog/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()