<?php
session_start();
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $role = $_POST['role'];
    $username = $_POST['username']; // Email for student, Username for admin
    $password = $_POST['password'];

    if ($role == 'student') {
        $sql = "SELECT id, name, password FROM students WHERE email = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            if (password_verify($password, $row['password'])) {
                $_SESSION['user_id'] = $row['id'];
                $_SESSION['user_name'] = $row['name'];
                $_SESSION['role'] = 'student';
                header("Location: ../dashboard.html");
            } else {
                echo "<script>alert('Invalid Password'); window.location.href='../login.html';</script>";
            }
        } else {
            echo "<script>alert('No student found with this email'); window.location.href='../login.html';</script>";
        }
    } else if ($role == 'admin') {
        $sql = "SELECT id, password FROM admin WHERE username = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            // Note: In the setup script I inserted 'admin123' as plain text for simplicity.
            // If we want consistent security, we should update that to a hash, or check plain text here.
            // For the user request "Simple", and the setup script provided:
            // "INSERT INTO admin ... VALUES ('admin', 'admin123')" -> This is plain text.
            if ($password === $row['password']) {
                $_SESSION['admin_id'] = $row['id'];
                $_SESSION['role'] = 'admin';
                header("Location: ../admin.html");
            } else {
                echo "<script>alert('Invalid Admin Password'); window.location.href='../login.html';</script>";
            }
        } else {
            echo "<script>alert('Admin not found'); window.location.href='../login.html';</script>";
        }
    }
    $conn->close();
}
?>