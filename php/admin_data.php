<?php
session_start();
include 'db.php';

header('Content-Type: application/json');

if (!isset($_SESSION['admin_id'])) {
    echo json_encode([]);
    exit();
}

$sql = "SELECT c.id, c.student_id, s.name as student_name, c.category, c.description, c.status, c.is_anonymous, c.created_at 
        FROM complaints c 
        JOIN students s ON c.student_id = s.id 
        ORDER BY c.created_at DESC";

$result = $conn->query($sql);

$complaints = [];

while ($row = $result->fetch_assoc()) {
    // If anonymous, hide name
    if ($row['is_anonymous'] == 1) {
        $row['student_name'] = "Anonymous";
    }
    $complaints[] = $row;
}

echo json_encode($complaints);

$conn->close();
?>