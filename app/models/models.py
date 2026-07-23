from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assignments = db.relationship('Assignment', backref='employee', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    assignments = db.relationship('Assignment', backref='task', lazy=True)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    shift = db.Column(db.String(20), nullable=False, default='Sáng') # Sáng / Chiều
    created_at = db.Column(db.DateTime, default=datetime.utcnow)