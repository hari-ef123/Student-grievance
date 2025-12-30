-- Database Creation
CREATE DATABASE IF NOT EXISTS grievance_db;
USE grievance_db;

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    is_anonymous TINYINT(1) DEFAULT 0,
    status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
    admin_remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Admin Table
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert a default admin (Password: admin123)
-- Note: In a real app, use password_hash(). For simplicity/demo as requested:
INSERT INTO admin (username, password) VALUES ('admin', 'admin123') 
ON DUPLICATE KEY UPDATE id=id;
