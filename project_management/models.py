
from app import db

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=True)
	created_at = db.Column(db.DateTime, default=db.func.now())
	tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan")
	files = db.Column(db.Text, nullable=True)  # Comma-separated list of file paths

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	is_done = db.Column(db.Boolean, default=False)
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
