<?php
session_start();
if (!isset($_SESSION['admin_id'])) {
    header("Location: login.html");
    exit();
}
include 'php/db.php'; // Path might need adjustment depending on where this file is saved. 
// Actually, if I save this as admin.php in root, path is php/db.php. 
// If I save it in php/admin.php, path is db.php.
// Let's decide to save it in php/admin.php to match dashboard.php
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Grievance System</title>
    <!-- Adjust CSS path since we are in php/ folder -->
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .table-container {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            color: white;
            min-width: 600px;
        }

        th,
        td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        th {
            background: rgba(255, 255, 255, 0.1);
            font-weight: 600;
        }

        tr:hover {
            background: rgba(255, 255, 255, 0.05);
        }

        select.status-select {
            padding: 5px;
            border-radius: 5px;
            border: none;
            background: rgba(255, 255, 255, 0.8);
            color: #333;
        }
    </style>
</head>

<body>
    <div class="navbar glass-card" style="position: sticky; top: 0; width: 95%; margin: 20px auto; z-index: 100;">
        <div class="logo"><i class="fas fa-user-shield"></i> Admin Panel</div>
        <div>
            <span style="margin-right: 15px;">Administrator</span>
            <a href="logout.php" class="btn btn-outline" style="padding: 5px 15px; font-size: 0.9rem;">Logout</a>
        </div>
    </div>

    <div class="container animate-fade-in" style="margin-top: 50px;">
        <!-- Stats -->
        <div class="grid-container mb-20">
            <div class="glass-card text-center" style="padding: 20px;">
                <h4>Total Complaints</h4>
                <p id="total-count" style="font-size: 2rem; font-weight: bold;">Loading...</p>
            </div>
            <div class="glass-card text-center" style="padding: 20px;">
                <h4>Pending Action</h4>
                <p id="pending-count" style="font-size: 2rem; font-weight: bold; color: #f39c12;">Loading...</p>
            </div>
        </div>

        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3>Student Complaints</h3>
                <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Search..." class="form-control"
                    style="width: 200px; padding: 8px;">
            </div>

            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Student</th>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Status / Action</th>
                            <th>Update</th>
                        </tr>
                    </thead>
                    <tbody id="complaints-table">
                        <tr>
                            <td colspan="6" class="text-center">Loading complaints...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let allComplaints = [];

        function loadComplaints() {
            fetch('admin_data.php')
                .then(res => res.json())
                .then(data => {
                    allComplaints = data;
                    renderTable(data);
                    updateStats(data);
                })
                .catch(err => {
                    console.error(err);
                    document.getElementById('complaints-table').innerHTML = `<tr><td colspan="6" class="text-center">Error loading data.</td></tr>`;
                });
        }

        function renderTable(data) {
            const tbody = document.getElementById('complaints-table');
            if (data.length > 0) {
                tbody.innerHTML = '';
                data.forEach(item => {
                    const row = `
                        <tr>
                            <td>#${item.id}</td>
                            <td>${item.student_name} ${item.is_anonymous == 1 ? '<i class="fas fa-user-secret" title="Anonymous"></i>' : ''}</td>
                            <td>${item.category}</td>
                            <td>${item.description}</td>
                            <td>
                                <select class="status-select" id="status-${item.id}">
                                    <option value="Pending" ${item.status === 'Pending' ? 'selected' : ''}>Pending</option>
                                    <option value="In Progress" ${item.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                                    <option value="Resolved" ${item.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                                </select>
                            </td>
                            <td>
                                <button onclick="updateStatus(${item.id})" class="btn btn-primary" style="padding: 5px 10px; font-size: 0.8rem;">Update</button>
                            </td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            } else {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center" style="padding: 30px;">No complaints found.</td></tr>`;
            }
        }

        function updateStats(data) {
            document.getElementById('total-count').innerText = data.length;
            const pending = data.filter(item => item.status === 'Pending').length;
            document.getElementById('pending-count').innerText = pending;
        }

        function updateStatus(id) {
            const newStatus = document.getElementById(`status-` + id).value;
            fetch('update_status.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id, status: newStatus })
            })
                .then(res => res.json())
                .then(data => {
                    alert(data.message);
                    loadComplaints();
                });
        }

        function filterTable() {
            const input = document.getElementById("searchInput").value.toLowerCase();
            const filtered = allComplaints.filter(item =>
                item.description.toLowerCase().includes(input) ||
                item.category.toLowerCase().includes(input) ||
                (item.student_name && item.student_name.toLowerCase().includes(input))
            );
            renderTable(filtered);
        }

        loadComplaints();
    </script>
</body>

</html>