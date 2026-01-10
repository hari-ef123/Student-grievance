<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: ../login.html");
    exit();
}

$user_id = $_SESSION['user_id'];
$user_name = $_SESSION['user_name'];

// Fetch Stats
$total_sql = "SELECT COUNT(*) as count FROM complaints WHERE student_id = ?";
$stmt = $conn->prepare($total_sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$total = $stmt->get_result()->fetch_assoc()['count'];

$pending_sql = "SELECT COUNT(*) as count FROM complaints WHERE student_id = ? AND status = 'Pending'";
$stmt = $conn->prepare($pending_sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$pending = $stmt->get_result()->fetch_assoc()['count'];

$resolved_sql = "SELECT COUNT(*) as count FROM complaints WHERE student_id = ? AND status = 'Resolved'";
$stmt = $conn->prepare($resolved_sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$resolved = $stmt->get_result()->fetch_assoc()['count'];

$stmt->close();
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Student Grievance System</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <div class="navbar glass-card" style="position: sticky; top: 0; width: 95%; margin: 20px auto; z-index: 100;">
        <div class="logo"><i class="fas fa-user-graduate"></i> Student Dashboard</div>
        <div>
            <span style="margin-right: 15px;">Welcome, <?php echo htmlspecialchars($user_name); ?>!</span>
            <a href="logout.php" class="btn btn-outline" style="padding: 5px 15px; font-size: 0.9rem;">Logout</a>
        </div>
    </div>

    <div class="container animate-fade-in" style="margin-top: 50px;">
        <!-- Stats Row -->
        <div class="grid-container">
            <div class="glass-card text-center">
                <i class="fas fa-file-alt fa-2x" style="color: #667eea; margin-bottom: 10px;"></i>
                <h3>Total Complaints</h3>
                <h2><?php echo $total; ?></h2>
            </div>
            <div class="glass-card text-center">
                <i class="fas fa-clock fa-2x" style="color: #f39c12; margin-bottom: 10px;"></i>
                <h3>Pending</h3>
                <h2><?php echo $pending; ?></h2>
            </div>
            <div class="glass-card text-center">
                <i class="fas fa-check-circle fa-2x" style="color: #2ecc71; margin-bottom: 10px;"></i>
                <h3>Resolved</h3>
                <h2><?php echo $resolved; ?></h2>
            </div>
        </div>

        <!-- Chart Section (Interesting Feature) -->
        <div class="glass-card" style="margin-top: 30px;">
            <h3><i class="fas fa-chart-pie"></i> Complaint Overview</h3>
            <div style="height: 300px; width: 100%;">
                <canvas id="complaintChart"></canvas>
            </div>
        </div>

        <!-- Actions Row -->
        <div style="margin-top: 30px; display: flex; gap: 20px; flex-wrap: wrap;">
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3><i class="fas fa-bullhorn"></i> Raise a New Complaint</h3>
                <p style="margin: 15px 0; opacity: 0.8;">Facing an issue? Submit your grievance here. We ensure privacy
                    and quick resolution.</p>
                <a href="../complaint.html" class="btn btn-primary">File Complaint</a>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 300px;">
                <h3><i class="fas fa-history"></i> Track Status</h3>
                <p style="margin: 15px 0; opacity: 0.8;">Check the real-time status of your submitted complaints with
                    admin remarks.</p>
                <a href="status.php" class="btn btn-outline" style="background: rgba(255,255,255,0.1);">View Status</a>
            </div>
        </div>
    </div>

    <script>
        // Chart.js Implementation
        const ctx = document.getElementById('complaintChart').getContext('2d');
        const complaintChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Resolved', 'In Progress'], // Simplified for visual
                datasets: [{
                    label: '# of Votes',
                    data: [<?php echo $pending; ?>, <?php echo $resolved; ?>, <?php echo ($total - $pending - $resolved); ?>],
                    backgroundColor: [
                        'rgba(243, 156, 18, 0.6)',
                        'rgba(46, 204, 113, 0.6)',
                        'rgba(52, 152, 219, 0.6)'
                    ],
                    borderColor: [
                        'rgba(243, 156, 18, 1)',
                        'rgba(46, 204, 113, 1)',
                        'rgba(52, 152, 219, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: 'white' }
                    }
                }
            }
        });
    </script>
</body>

</html>