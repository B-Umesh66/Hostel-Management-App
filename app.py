
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'KSU66'

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Umesh2004",
        database="hostel_db"
    )
    return connection

# Home page
@app.route('/')
def home():
    return render_template('HomePage.html')

# Student login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['role'] = 'student'
            return redirect(url_for('student_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('StudentLogin.html', msg=msg)

# Student signup
@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['select_gender']
        phno = request.form['phno']
        age = request.form['age']
        dob = request.form['dob']
        address = request.form['address']
        college_name = request.form['college_name']
        branch = request.form['branch']
        student_id = request.form['student_id']
        year_of_study = request.form['year_of_study']
        hostel = request.form['hostel_name']
        room_no = request.form['room_no']
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        else:
            cursor.execute('INSERT INTO students (name, email, gender, phno, age, dob, address, college_name, branch, student_id, year_of_study, hostel, room_no, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, email, gender, phno, age, dob, address, college_name, branch, student_id, year_of_study, hostel, room_no, username, password))
            connection.commit()
            msg = 'You have successfully registered!'
    
    return render_template('Student_SignUp.html', msg=msg)

# Student page
@app.route('/student_page')
def student_page():
    if 'loggedin' in session and session['role'] == 'student':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students WHERE username = %s', (session['username'],))
        student = cursor.fetchone()
        return render_template('StudentPage.html', student=student)
    return redirect(url_for('student_login'))

# Generate outpass
@app.route('/generate_outpass', methods=['GET', 'POST'])
def generate_outpass():
    if 'loggedin' in session and session['role'] == 'student':
        msg = ''
        if request.method == 'POST':
            reason = request.form['reason']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT student_id FROM students WHERE username = %s', (session['username'],))
            student = cursor.fetchone()
            student_id = student['student_id']
            
            cursor.execute('INSERT INTO outpass_requests (student_id, reason, from_date, to_date) VALUES (%s, %s, %s, %s)', (student_id, reason, from_date, to_date))
            connection.commit()
            msg = 'Outpass request submitted successfully!'
        return render_template('Generate_outpass.html', msg=msg)
    return redirect(url_for('student_login'))

# Change Room Request
@app.route('/change_room_request', methods=['GET', 'POST'])
def change_room_request():
    if 'loggedin' in session and session['role'] == 'student':
        msg = ''
        if request.method == 'POST':
            new_room_no = request.form['new_room_no']
            reason = request.form['reason']
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT student_id, room_no FROM students WHERE username = %s', (session['username'],))
            student = cursor.fetchone()
            student_id = student['student_id']
            current_room_no = student['room_no']
            
            cursor.execute('INSERT INTO room_change_requests (student_id, current_room_no, new_room_no, reason) VALUES (%s, %s, %s, %s)', (student_id, current_room_no, new_room_no, reason))
            connection.commit()
            msg = 'Room change request submitted successfully!'
        return render_template('Change_Room.html', msg=msg)
    return redirect(url_for('student_login'))

# Change Hostel Request
@app.route('/change_hostel_request', methods=['GET', 'POST'])
def change_hostel_request():
    if 'loggedin' in session and session['role'] == 'student':
        msg = ''
        if request.method == 'POST':
            new_hostel = request.form['new_hostel_name']
            reason = request.form['reason']
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT student_id, hostel FROM students WHERE username = %s', (session['username'],))
            student = cursor.fetchone()
            student_id = student['student_id']
            current_hostel = student['hostel']
            
            cursor.execute('INSERT INTO hostel_change_requests (student_id, current_hostel, new_hostel, reason) VALUES (%s, %s, %s, %s)', (student_id, current_hostel, new_hostel, reason))
            connection.commit()
            msg = 'Hostel change request submitted successfully!'
        return render_template('Change_Hostel.html', msg=msg)
    return redirect(url_for('student_login'))

# Warden login
@app.route('/warden_login', methods=['GET', 'POST'])
def warden_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM wardens WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['role'] = 'warden'
            return redirect(url_for('warden_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('WardenLogin.html', msg=msg)

# Warden signup
@app.route('/warden_signup', methods=['GET', 'POST'])
def warden_signup():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['select_gender']
        phno = request.form['phno']
        age = request.form['age']
        dob = request.form['dob']
        address = request.form['address']
        warden_id = request.form['warden_id']
        hostel_name = request.form['hostel_name']
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM wardens WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        else:
            cursor.execute('INSERT INTO wardens (name, email, gender, phno, age, dob, address, warden_id, hostel_name, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, email, gender, phno, age, dob, address, warden_id, hostel_name, username, password))
            connection.commit()
            msg = 'You have successfully registered!'
    
    return render_template('Warden_SignUp.html', msg=msg)

# Warden page
@app.route('/warden_page')
def warden_page():
    if 'loggedin' in session and session['role'] == 'warden':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM wardens WHERE username = %s', (session['username'],))
        warden = cursor.fetchone()
        return render_template('WardenPage.html', warden=warden)
    return redirect(url_for('warden_login'))

# Outpass approval
@app.route('/outpass_approval', methods=['GET', 'POST'])
def outpass_approval():
    if 'loggedin' in session and session['role'] == 'warden':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute('SELECT hostel_name FROM wardens WHERE username = %s', (session['username'],))
        warden = cursor.fetchone()
        hostel_name = warden['hostel_name']

        if request.method == 'POST':
            request_id = request.form['request_id']
            action = request.form['action']
            cursor.execute('UPDATE outpass_requests SET status = %s WHERE id = %s', (action, request_id))
            connection.commit()
            return redirect(url_for('outpass_approval'))

        cursor.execute("""
            SELECT o.* 
            FROM outpass_requests o
            JOIN students s ON o.student_id = s.student_id
            WHERE s.hostel = %s
        """, (hostel_name,))
        requests = cursor.fetchall()
        return render_template('Outpass_approval.html', requests=requests)
    return redirect(url_for('warden_login'))

# Room Change Approval
@app.route('/room_change_approval', methods=['GET', 'POST'])
def room_change_approval():
    if 'loggedin' in session and session['role'] == 'warden':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute('SELECT hostel_name FROM wardens WHERE username = %s', (session['username'],))
        warden = cursor.fetchone()
        hostel_name = warden['hostel_name']

        if request.method == 'POST':
            request_id = request.form['request_id']
            action = request.form['action']
            cursor.execute('UPDATE room_change_requests SET status = %s WHERE id = %s', (action, request_id))
            connection.commit()

            if action == 'approved':
                cursor.execute('SELECT student_id, new_room_no FROM room_change_requests WHERE id = %s', (request_id,))
                req = cursor.fetchone()
                cursor.execute('UPDATE students SET room_no = %s WHERE student_id = %s', (req['new_room_no'], req['student_id']))
                connection.commit()

            return redirect(url_for('room_change_approval'))

        cursor.execute("""
            SELECT r.* 
            FROM room_change_requests r
            JOIN students s ON r.student_id = s.student_id
            WHERE s.hostel = %s
        """, (hostel_name,))
        requests = cursor.fetchall()
        return render_template('hostel_room_change_approval.html', requests=requests)
    return redirect(url_for('warden_login'))

# Admin login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['role'] = 'admin'
            return redirect(url_for('admin_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('AdminLogin.html', msg=msg)

# Admin page
@app.route('/admin_page')
def admin_page():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE username = %s', (session['username'],))
        admin = cursor.fetchone()
        return render_template('AdminPage.html', admin=admin)
    return redirect(url_for('admin_login'))

# Hostel Change Approval
@app.route('/hostel_change_approval', methods=['GET', 'POST'])
def hostel_change_approval():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            request_id = request.form['request_id']
            action = request.form['action']
            cursor.execute('UPDATE hostel_change_requests SET status = %s WHERE id = %s', (action, request_id))
            connection.commit()

            if action == 'approved':
                cursor.execute('SELECT student_id, new_hostel FROM hostel_change_requests WHERE id = %s', (request_id,))
                req = cursor.fetchone()
                cursor.execute('UPDATE students SET hostel = %s, room_no = NULL WHERE student_id = %s', (req['new_hostel'], req['student_id']))
                connection.commit()

            return redirect(url_for('hostel_change_approval'))

        cursor.execute('SELECT * FROM hostel_change_requests')
        requests = cursor.fetchall()
        return render_template('hostel_change_approval.html', requests=requests)
    return redirect(url_for('admin_login'))

# View Students
@app.route('/view_students')
def view_students():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        return render_template('view_students.html', students=students)
    return redirect(url_for('admin_login'))

# View Wardens
@app.route('/view_wardens')
def view_wardens():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM wardens')
        wardens = cursor.fetchall()
        return render_template('view_wardens.html', wardens=wardens)
    return redirect(url_for('admin_login'))

# Contact Us
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
