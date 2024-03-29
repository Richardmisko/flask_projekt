from flask_sqlalchemy import SQLAlchemy   # 301 , 3:20

db = SQLAlchemy()

class Article(db.Model): 
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	content = db.Column(db.String)

# 301, 3:20

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True) 
	username = db.Column(db.String, unique = True)
	password = db.Column(db.String)
