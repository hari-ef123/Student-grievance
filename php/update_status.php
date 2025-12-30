<?php
session_start();
include 'db.php';

if (!isset($_SESSION['admin_id'])) {
    die("Unauthorized");
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Expecting JSON input for AJAX or Form
    // For this simple plan, I'll support JSON input which is better for the 'Futuristic status update'

    $input = json_decode(file_get_contents('php://input'), true);

    if ($input) {
        $id = $input['id'];
        $status = $input['status'];

        $sql = "UPDATE complaints SET status = ? WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("si", $status, $id);

        if ($stmt->execute()) {
            echo json_encode(["message" => "Status updated successfully"]);
        } else {
            echo json_encode(["message" => "Error updating status"]);
        }
        $stmt->close();
    } else {
        // Fallback or Error
        echo json_encode(["message" => "Invalid Input"]);
    }

    $conn->close();
}
?>