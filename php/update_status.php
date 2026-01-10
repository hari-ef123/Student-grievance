<?php
session_start();
include 'db.php';

header('Content-Type: application/json');

// Check if admin is logged in
if (!isset($_SESSION['admin_id'])) {
    http_response_code(403);
    echo json_encode(["message" => "Unauthorized"]);
    exit();
}

// Get JSON input
$data = json_decode(file_get_contents("php://input"), true);

if (isset($data['id']) && isset($data['status'])) {
    $id = $data['id'];
    $status = $data['status'];

    $sql = "UPDATE complaints SET status = ? WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("si", $status, $id);

    if ($stmt->execute()) {
        echo json_encode(["message" => "Status updated successfully!"]);
    } else {
        echo json_encode(["message" => "Error updating status."]);
    }
    $stmt->close();
} else {
    echo json_encode(["message" => "Invalid input."]);
}

$conn->close();
?>