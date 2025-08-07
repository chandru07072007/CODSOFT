# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_post.id'))
    candidate_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    resume_link = db.Column(db.String(255))
        