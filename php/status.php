<?php
session_start();
if (!isset($_SESSION['user_id'])) {
    header("Location: ../login.html");
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Track Status - Grievance System</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>

<body>
    <div class="navbar glass-card" style="position: sticky; top: 0; width: 95%; margin: 20px auto; z-index: 100;">
        <div class="logo"><i class="fas fa-university"></i> SGS</div>
        <a href="dashboard.php" class="btn btn-outline" style="padding: 8px 20px;">Back to Dashboard</a>
    </div>

    <div class="container animate-fade-in" style="margin-top: 50px;">
        <h2 class="text-center" style="color: white; margin-bottom: 30px;">Your Complaints Status</h2>

        <div id="status-container">
            <div class="glass-card text-center">
                <p>Loading your complaints...</p>
            </div>
        </div>
    </div>

    <script>
        // Fetch status from backend API
        fetch('get_status.php')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('status-container');
                if (data.length > 0) {
                    container.innerHTML = '';
                    data.forEach(item => {
                        // Determine status color
                        let badgeClass = 'status-Pending';
                        if (item.status === 'In Progress') badgeClass = 'status-In';
                        if (item.status === 'Resolved') badgeClass = 'status-Resolved';

                        const html = `
                        <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <div style="text-align: left;">
                                <h3 style="margin: 0 0 10px 0; color: #667eea;">${item.category}</h3>
                                <p style="font-size: 0.95rem; opacity: 0.9; margin-bottom: 8px;">${item.description}</p>
                                <p style="font-size: 0.8rem; opacity: 0.6;">Submitted on: ${item.created_at}</p>
                                ${item.admin_remark ? `<div style="margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 5px;"><strong style="color: #f1c40f;">Admin Remark:</strong> ${item.admin_remark}</div>` : ''}
                            </div>
                            <div class="text-center" style="min-width: 120px;">
                                <span class="status-badge ${badgeClass}" style="padding: 8px 15px; border-radius: 20px; font-size: 0.85rem;">${item.status}</span>
                            </div>
                        </div>
                       `;
                        container.innerHTML += html;
                    });
                } else {
                    container.innerHTML = '<div class="glass-card text-center"><p>No complaints found.</p></div>';
                }
            })
            .catch(err => {
                console.error(err);
                document.getElementById('status-container').innerHTML = '<div class="glass-card text-center"><p>Error loading data.</p></div>';
            });
    </script>
</body>

</html>