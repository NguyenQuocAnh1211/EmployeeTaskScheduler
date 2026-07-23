from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import Employee, Task, Assignment

main = Blueprint('main', __name__)

# --- THUẬT TOÁN TỰ ĐỘNG CHỌN NGƯỜI ÍT VIỆC NHẤT ---
def get_auto_assigned_employee_id():
    employees = Employee.query.all()
    if not employees:
        return None
    
    # Tìm nhân viên có số ca/task trong bảng Assignment ít nhất
    least_busy_employee = min(
        employees,
        key=lambda emp: Assignment.query.filter_by(employee_id=emp.id).count()
    )
    return least_busy_employee.id

# --- 1. CHỨC NĂNG THÊM NGƯỜI DÙNG MỚI (LƯU DB) ---
@main.route('/add-employee', methods=['POST'])
@main.route('/add-employee', methods=['POST'])
def add_employee():
    emp_name = request.form.get('employee_name')
    if emp_name and emp_name.strip():
        # Tạo object và lưu trực tiếp vào CSDL
        new_emp = Employee(name=emp_name.strip())
        db.session.add(new_emp)
        db.session.commit()
        flash('Đã thêm nhân viên thành công!', 'success')

    return redirect(url_for('main.dashboard'))

# --- 2. CHỨC NĂNG PHÂN CÔNG (THỦ CÔNG HOẶC TỰ ĐỘNG) ---
@main.route('/assign-task', methods=['POST'])
def assign_task():
    employee_id = request.form.get('employee_id')
    task_id = request.form.get('task_id')
    shift = request.form.get('shift', 'Sáng')

    # Nếu người dùng chọn "✨ Tự động phân công" (value là 'auto')
    if employee_id == 'auto':
        employee_id = get_auto_assigned_employee_id()

    # Kiểm tra xem có đủ data để lưu không
    if employee_id and task_id:
        new_assign = Assignment(
            employee_id=int(employee_id),
            task_id=int(task_id),
            shift=shift
        )
        db.session.add(new_assign)
        db.session.commit()
        flash('Đã phân công thành công!', 'success')
    else:
        flash('Vui lòng tạo nhân viên/công việc trước!', 'danger')

    return redirect(url_for('tasks.dashboard'))

# --- 3. DẠY TRANG DASHBOARD LẤY DỮ LIỆU THẬT TỪ DB ---
@main.route('/')
@main.route('/dashboard')
def dashboard():
    employees = Employee.query.all()
    tasks = Task.query.all()
    assignments = Assignment.query.order_by(Assignment.created_at.desc()).all()
    
    return render_template('dashboard.html', 
                           employees=employees, 
                           tasks=tasks, 
                           assignments=assignments)