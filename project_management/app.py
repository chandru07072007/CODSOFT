# Edit project route

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'your_secret_key'  # Needed for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan")
    files = db.Column(db.Text, nullable=True)  # Comma-separated list of file paths

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Routes
@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects'))
    return render_template('edit_project.html', project=project)
@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    description = request.form['description']
    files = request.files.getlist('project_files')
    uploaded_files = []
    for file in files:
        if file and file.filename:
            # Handle subfolders in filename (e.g., 'folder/file.txt')
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            save_dir = os.path.dirname(save_path)
            os.makedirs(save_dir, exist_ok=True)
            file.save(save_path)
            uploaded_files.append(file.filename)
    if uploaded_files:
        flash(f"Uploaded files: {', '.join(uploaded_files)}", 'success')
    files_str = ','.join(uploaded_files) if uploaded_files else None
    new_project = Project(name=name, description=description, files=files_str)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('projects'))

@app.route('/delete_project/<int:id>')
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


# List all projects
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects_list.html', projects=projects)

# Project detail
@app.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    # Prepare file links for template
    file_links = []
    if project.files:
        for f in project.files.split(','):
            file_links.append(f)
    return render_template('projects.html', project=project, file_links=file_links)

@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    title = request.form['title']
    new_task = Task(title=title, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('project_detail', id=project_id))

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('project_detail', id=task.project_id))
@app.route('/tasks')
def tasks():
    status = request.args.get('status')
    projects = Project.query.all()

    if status == "completed":
        tasks = Task.query.filter_by(is_done=True).all()
    elif status == "pending":
        tasks = Task.query.filter_by(is_done=False).all()
    else:
        tasks = Task.query.all()

    return render_template('tasks.html', tasks=tasks, projects=projects)

@app.route('/add_task_global', methods=['POST'])
def add_task_global():
    title = request.form['title']
    project_id = request.form['project_id']
    new_task = Task(title=title, project_id=project_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))
@app.route('/toggle_task_ajax/<int:task_id>', methods=['POST'])
def toggle_task_ajax(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return {"success": True, "is_done": task.is_done}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
