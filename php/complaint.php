<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user_id'])) {
    // If not logged in, redirect
    header("Location: ../login.html");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $student_id = $_SESSION['user_id'];
    $category = $_POST['category'];
    $description = $_POST['description'];

    // Check if anonymous checkbox is checked (value '1') or not
    $is_anonymous = isset($_POST['is_anonymous']) ? 1 : 0;

    $sql = "INSERT INTO complaints (student_id, category, description, is_anonymous) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("issi", $student_id, $category, $description, $is_anonymous);

    if ($stmt->execute()) {
        echo "<script>alert('Complaint Submitted Successfully!'); window.location.href='../dashboard.html';</script>";
    } else {
        echo "Error: " . $conn->error;
    }

    $stmt->close();
    $conn->close();
}
?>