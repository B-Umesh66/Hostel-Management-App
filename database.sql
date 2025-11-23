CREATE DATABASE pythonlogin;
USE pythonlogin;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
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
