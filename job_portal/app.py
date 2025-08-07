from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ========================
# Models
# ========================
class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50))
    description = db.Column(db.Text)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_post.id'), nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    applicant_email = db.Column(db.String(100), nullable=False)
    resume_filename = db.Column(db.String(200))

# ========================
# Routes
# ========================
@app.route('/')
def home():
    jobs = JobPost.query.limit(10).all()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job = JobPost(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            salary=request.form['salary'],
            description=request.form['description']
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post_job.html')

@app.route('/jobs')
def job_list():
    jobs = JobPost.query.all()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/job_detail')
def job_detail():
    applications = Application.query.all()
    return render_template('job.html', applications=applications)

@app.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    job = JobPost.query.get_or_404(job_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        resume = request.files['resume']

        if not resume or not resume.filename.endswith('.pdf'):
            flash('Please upload a valid PDF resume.', 'error')
            return redirect(request.url)

        filename = secure_filename(resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume.save(resume_path)

        application = Application(
            job_id=job.id,
            applicant_name=name,
            applicant_email=email,
            resume_filename=filename
        )
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('apply_job.html', job=job)

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return "Resume uploaded successfully!"
        else:
            return "Only PDF files are allowed."
    return render_template('upload_resume.html')

@app.route('/candidate_dashboard')
def candidate_dashboard():
    applications = Application.query.all()
    return render_template('candidate_dashboard.html', applications=applications)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# ========================
# Run App
# ========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
