from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Bugtracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        task_type = request.form['task_type']
        priority = request.form['priority']
        status = request.form['status']
        description = request.form['description']
        creator_id = 1 

        new_task = Task(title=title, task_type=task_type, priority=priority, status=status, description=description, creator_id=creator_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('create_task.html')

@app.route('/task/<int:task_id>')
def task_details(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_details.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
