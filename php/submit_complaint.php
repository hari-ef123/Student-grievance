<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: ../login.html");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $student_id = $_SESSION['user_id'];
    $category = $_POST['category'];
    $description = $_POST['description'];
    $is_anonymous = isset($_POST['is_anonymous']) ? 1 : 0;

    // --- Smart Routing Simulation ---
    // In a real system, this might assign to a specific admin ID.
    // Here, we'll just add an initial admin remark or log it.
    $admin_remark = "System: Pending review.";
    if ($category == 'Academic') {
        $admin_remark = "System: Auto-routed to HOD for review.";
    } elseif ($category == 'Infrastructure') {
        $admin_remark = "System: Auto-routed to Maintenance Dept.";
    } elseif ($category == 'Canteen') {
        $admin_remark = "System: Auto-routed to Canteen Manager.";
    }

    $status = 'Pending';

    $sql = "INSERT INTO complaints (student_id, category, description, is_anonymous, status, admin_remark) VALUES (?, ?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);

    if ($stmt) {
        $stmt->bind_param("ississ", $student_id, $category, $description, $is_anonymous, $status, $admin_remark);

        if ($stmt->execute()) {
            echo "<script>alert('Complaint Submitted Successfully! Tracking started.'); window.location.href='../php/dashboard.php';</script>";
        } else {
            echo "Error: " . $stmt->error;
        }
        $stmt->close();
    } else {
        echo "Error preparing statement: " . $conn->error;
    }

    $conn->close();
}
?>