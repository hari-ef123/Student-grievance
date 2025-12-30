<?php
session_start();
include 'db.php';

header('Content-Type: application/json');

if (!isset($_SESSION['user_id'])) {
    echo json_encode([]);
    exit();
}

$student_id = $_SESSION['user_id'];

$sql = "SELECT category, description, status, admin_remark, created_at FROM complaints WHERE student_id = ? ORDER BY created_at DESC";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $student_id);
$stmt->execute();
$result = $stmt->get_result();

$complaints = [];

while ($row = $result->fetch_assoc()) {
    $complaints[] = $row;
}

echo json_encode($complaints);

$stmt->close();
$conn->close();
?>