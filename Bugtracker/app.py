from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Bugtracker'
app.config['SECRET_KEY'] = 'your_secret_key'  
db = SQLAlchemy(app)


migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) 


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  
    priority = db.Column(db.String(10), nullable=True) 
    status = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', foreign_keys=[creator_id])
    assignee = db.relationship('User', foreign_keys=[assignee_id])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("Form Data Submitted:", request.form)

     
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
     
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
     
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
      
        user = User.query.filter_by(username=username).first()

        
        if user and check_password_hash(user.password, password):
            login_user(user) 

           
            tasks = Task.query.all()
            return render_template('index.html', tasks=tasks)
        
        flash('Invalid credentials!', 'danger')
        return redirect(url_for('login'))  

    return render_template('login.html')


@app.route('/tasks', methods=['POST'])
@login_required
def create_task():
    try:
        data = request.form
        new_task = Task(
            type=data['type'],
            priority=data['priority'],
            status=data['status'],
            title=data['title'],
            description=data.get('description', 'No description'),
            creator_id=current_user.id,
            assignee_id=int(data.get('assignee_id')) if data.get('assignee_id') else None
        )
        db.session.add(new_task)
        db.session.commit()

       
        return jsonify({'message': 'Task created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    user = {
        'id': current_user.id,
        'username': current_user.username
    }
    return jsonify(user), 200

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list), 200

@app.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    tasks = Task.query.all()
    task_list = [
        {
            'id': task.id,
            'type': task.type,
            'priority': task.priority,
            'status': task.status,
            'title': task.title,
            'description': task.description,
            'creator_name': task.creator.username,
            'assignee_name': User.query.get(task.assignee_id).username if task.assignee_id else 'Unassigned',
            'created_at': task.created_at,
            'updated_at': task.updated_at
        }
        for task in tasks
    ]
    return jsonify(task_list), 200
@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.all() 

    return render_template('index.html', tasks=tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found!'}), 404

     
        data = request.get_json()

    
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)
        task.assignee_id = data.get('assignee_id', task.assignee_id)

        db.session.commit()
        return jsonify({'message': 'Task updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    
    if current_user.role != 'manager':
        return jsonify({"message": "You do not have permission to delete tasks"}), 403

   
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200 

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('register'))


if __name__ == "__main__":
    app.run(port=5004, debug=True)
