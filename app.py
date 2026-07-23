from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='app/templates') # Hoặc 'templates' tùy cấu trúc thư mục của bạn

employees = []    
tasks = []        
assignments = []  

# Hàm lấy khoảng ngày (Từ Thứ 2 đến Chủ Nhật)
def get_week_range(reference_date):
    start_of_week = reference_date - timedelta(days=reference_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

@app.route('/')
def dashboard():
    try:
        week_offset = int(request.args.get('week_offset', 0))
    except ValueError:
        week_offset = 0

    # Lấy ngày hôm nay
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_display = datetime.now().strftime('%d/%m/%Y')

    current_date = datetime.now() + timedelta(weeks=week_offset)
    start_of_week, end_of_week = get_week_range(current_date)

    total_employees = len(employees)
    total_tasks = len(tasks)
    total_assignments = len(assignments)

    # 1. LỌC DANH SÁCH CÔNG VIỆC HÔM NAY
    today_tasks = []
    for assign in assignments:
        if assign['work_date'] == today_date:
            shift_text = "Ca Sáng" if assign['shift'] == 'sang' else "Ca Chiều"
            today_tasks.append({
                'employee_name': assign['employee_name'],
                'task_title': assign['task_title'],
                'shift': shift_text
            })

    total_today_tasks = len(today_tasks)

    # 2. GOM NHÓM LỊCH THEO TUẦN
    schedule_matrix = []
    for emp in employees:
        emp_schedule = {
            'employee_name': emp['name'],
            'thu_2': [], 'thu_3': [], 'thu_4': [], 'thu_5': [], 'thu_6': [], 'thu_7': []
        }
        
        for assign in assignments:
            if str(assign['employee_id']) == str(emp['id']):
                assign_date = datetime.strptime(assign['work_date'], '%Y-%m-%d')
                
                if start_of_week.date() <= assign_date.date() <= end_of_week.date():
                    weekday = assign_date.weekday()
                    weekday_map = {0: 'thu_2', 1: 'thu_3', 2: 'thu_4', 3: 'thu_5', 4: 'thu_6', 5: 'thu_7'}
                    day_key = weekday_map.get(weekday)
                    
                    if day_key:
                        shift_text = "Sáng" if assign['shift'] == 'sang' else "Chiều"
                        emp_schedule[day_key].append(f"{assign['task_title']} ({shift_text})")
                    
        schedule_matrix.append(emp_schedule)

    week_range_str = f"{start_of_week.strftime('%d/%m/%Y')} - {end_of_week.strftime('%d/%m/%Y')}"

    return render_template('dashboard.html', 
                           employees=employees, 
                           tasks=tasks, 
                           schedule_matrix=schedule_matrix,
                           today_tasks=today_tasks,
                           total_today_tasks=total_today_tasks,
                           today_display=today_display,
                           total_employees=total_employees,
                           total_tasks=total_tasks,
                           total_assignments=total_assignments,
                           week_offset=week_offset,
                           week_range_str=week_range_str)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form.get('employee_name')
    role = request.form.get('employee_role')
    if name:
        employees.append({'id': len(employees) + 1, 'name': name, 'role': role})
    return redirect(url_for('dashboard'))

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('task_title')
    desc = request.form.get('task_desc')
    if title:
        tasks.append({'id': len(tasks) + 1, 'title': title, 'desc': desc})
    return redirect(url_for('dashboard'))

@app.route('/assign', methods=['POST'])
def assign():
    employee_id = request.form.get('employee_id')
    task_id = request.form.get('task_id')
    work_date = request.form.get('work_date')
    shift = request.form.get('shift')
    
    if employee_id and task_id and work_date:
        emp_obj = next((e for e in employees if str(e['id']) == str(employee_id)), None)
        task_obj = next((t for t in tasks if str(t['id']) == str(task_id)), None)
        
        if emp_obj and task_obj:
            assignments.append({
                'employee_id': employee_id,
                'employee_name': emp_obj['name'],
                'task_title': task_obj['title'],
                'work_date': work_date,
                'shift': shift
            })
            
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)