CREATE DATABASE pythonlogin;
USE pythonlogin;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(150),
    phno VARCHAR(25),
    gender VARCHAR(20),
    age INT,
    dob DATE,
    address TEXT,
    college_name VARCHAR(255),
    branch VARCHAR(255),
    student_id VARCHAR(100),
    year_of_study VARCHAR(50),
    hostel VARCHAR(255),
    room_no VARCHAR(50)
);

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE wardens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE hostel_change_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    current_hostel VARCHAR(255) NOT NULL,
    requested_hostel VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE room_change_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    current_room VARCHAR(255) NOT NULL,
    requested_room VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE outpass_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (student_id) REFERENCES students(id)
);
