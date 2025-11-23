
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Umesh2004",
        database="pythonlogin"
    )
    return connection

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            gender VARCHAR(50),
            phno VARCHAR(20),
            age INT,
            dob DATE,
            address TEXT,
            college_name VARCHAR(255),
            branch VARCHAR(255),
            student_id VARCHAR(255) NOT NULL UNIQUE,
            year_of_study VARCHAR(50),
            hostel VARCHAR(255),
            room_no VARCHAR(50),
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wardens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            gender VARCHAR(50),
            phno VARCHAR(20),
            age INT,
            dob DATE,
            address TEXT,
            warden_id VARCHAR(255) NOT NULL UNIQUE,
            hostel_name VARCHAR(255),
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outpass_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(255),
            reason TEXT,
            from_date DATE,
            to_date DATE,
            status VARCHAR(50) DEFAULT 'pending',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room_change_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(255),
            current_room_no VARCHAR(50),
            new_room_no VARCHAR(50),
            reason TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostel_change_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(255),
            current_hostel VARCHAR(255),
            new_hostel VARCHAR(255),
            reason TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)
    
    cursor.execute('''
        INSERT INTO admins (name, username, password)
        SELECT * FROM (SELECT 'admin' AS name, 'admin' AS username, 'admin' AS password) AS tmp
        WHERE NOT EXISTS (
            SELECT username FROM admins WHERE username = 'admin'
        ) LIMIT 1;
    ''')

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    create_tables()
