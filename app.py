from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for session)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE name = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['name']
            return redirect(url_for('student_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('StudentLogin.html', msg=msg)

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE name = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO students VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('Student_SignUp.html', msg=msg)

@app.route('/student_page')
def student_page():
    if 'loggedin' in session:
        return render_template('StudentPage.html', username=session['username'])
    return redirect(url_for('student_login'))

@app.route('/change_hostel', methods=['GET', 'POST'])
def change_hostel():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'hostel' in request.form and 'reason' in request.form:
            hostel = request.form['hostel']
            reason = request.form['reason']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO hostel_change_requests VALUES (NULL, %s, %s, %s, %s, %s)', (session['id'], 'current_hostel', hostel, reason, 'pending',))
            mysql.connection.commit()
            msg = 'Request submitted successfully!'
        return render_template('ChangeHostel_request.html', msg=msg)
    return redirect(url_for('student_login'))

@app.route('/change_room', methods=['GET', 'POST'])
def change_room():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'requested_room' in request.form and 'reason' in request.form:
            requested_room = request.form['requested_room']
            reason = request.form['reason']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO room_change_requests VALUES (NULL, %s, %s, %s, %s, %s)', (session['id'], 'current_room', requested_room, reason, 'pending',))
            mysql.connection.commit()
            msg = 'Request submitted successfully!'
        return render_template('ChangeRoom_request.html', msg=msg)
    return redirect(url_for('student_login'))

@app.route('/generate_outpass', methods=['GET', 'POST'])
def generate_outpass():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'from_date' in request.form and 'to_date' in request.form and 'reason' in request.form:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            reason = request.form['reason']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO outpass_requests VALUES (NULL, %s, %s, %s, %s, %s)', (session['id'], from_date, to_date, reason, 'pending',))
            mysql.connection.commit()
            msg = 'Outpass request submitted successfully!'
        return render_template('Generate_outpass.html', msg=msg)
    return redirect(url_for('student_login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE name = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['name']
            return redirect(url_for('admin_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('AdminLogin.html', msg=msg)

@app.route('/admin_page')
def admin_page():
    if 'loggedin' in session:
        return render_template('AdminPage.html', username=session['username'])
    return redirect(url_for('admin_login'))

@app.route('/hostel_change_approval')
def hostel_change_approval():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hostel_change_requests')
        requests = cursor.fetchall()
        return render_template('hostel_change_approval.html', requests=requests)
    return redirect(url_for('admin_login'))

@app.route('/approve_hostel_change/<int:request_id>')
def approve_hostel_change(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE hostel_change_requests SET status = "approved" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('hostel_change_approval'))
    return redirect(url_for('admin_login'))

@app.route('/reject_hostel_change/<int:request_id>')
def reject_hostel_change(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE hostel_change_requests SET status = "rejected" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('hostel_change_approval'))
    return redirect(url_for('admin_login'))

@app.route('/warden_login', methods=['GET', 'POST'])
def warden_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM wardens WHERE name = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['name']
            return redirect(url_for('warden_page'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('WardenLogin.html', msg=msg)

@app.route('/warden_page')
def warden_page():
    if 'loggedin' in session:
        return render_template('WardenPage.html', username=session['username'])
    return redirect(url_for('warden_login'))

@app.route('/room_change_approval')
def room_change_approval():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM room_change_requests')
        requests = cursor.fetchall()
        return render_template('hostel_room_change_approval.html', requests=requests)
    return redirect(url_for('warden_login'))

@app.route('/approve_room_change/<int:request_id>')
def approve_room_change(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE room_change_requests SET status = "approved" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('room_change_approval'))
    return redirect(url_for('warden_login'))

@app.route('/reject_room_change/<int:request_id>')
def reject_room_change(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE room_change_requests SET status = "rejected" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('room_change_approval'))
    return redirect(url_for('warden_login'))

@app.route('/outpass_approval')
def outpass_approval():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM outpass_requests')
        requests = cursor.fetchall()
        return render_template('Outpass_approval.html', requests=requests)
    return redirect(url_for('warden_login'))

@app.route('/approve_outpass/<int:request_id>')
def approve_outpass(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE outpass_requests SET status = "approved" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('outpass_approval'))
    return redirect(url_for('warden_login'))

@app.route('/reject_outpass/<int:request_id>')
def reject_outpass(request_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE outpass_requests SET status = "rejected" WHERE id = %s', (request_id,))
        mysql.connection.commit()
        return redirect(url_for('outpass_approval'))
    return redirect(url_for('warden_login'))

if __name__ == '__main__':
    app.run(debug=True)
