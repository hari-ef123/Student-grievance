// Mock Data for Demo Mode (LocalStorage Enabled)

// Helper to check if we are in Demo Mode
function isDemoMode() {
    return window.location.protocol === 'file:';
}

const defaultStats = {
    total: 12,
    pending: 3,
    resolved: 9
};

const defaultComplaints = [
    {
        id: 101,
        student_name: "John Doe",
        category: "Academic",
        description: "Missing marks in subject code CS101. I submitted the assignment on time.",
        status: "Pending",
        admin_remark: null,
        created_at: "2023-10-25 10:30:00",
        is_anonymous: 0
    },
    {
        id: 102,
        student_name: "Jane Smith",
        category: "Infrastructure",
        description: "Fan not working in Room 304. It makes a loud noise.",
        status: "In Progress",
        admin_remark: "Maintenance team assigned. Verified the issue.",
        created_at: "2023-10-24 14:15:00",
        is_anonymous: 0
    },
    {
        id: 103,
        student_name: "Anonymous",
        category: "Canteen",
        description: "Food quality was poor yesterday. Rice was undercooked.",
        status: "Resolved",
        admin_remark: "Vendor notified. Refund processed for affected students.",
        created_at: "2023-10-22 09:00:00",
        is_anonymous: 1
    }
];

// --- STORAGE KEY ---
const DB_KEY = 'SGS_DEMO_DB';

// --- DATA ACCESS LAYER ---

function getComplaints() {
    const stored = localStorage.getItem(DB_KEY);
    if (!stored) {
        // Init with default
        localStorage.setItem(DB_KEY, JSON.stringify(defaultComplaints));
        return defaultComplaints;
    }
    return JSON.parse(stored);
}

function saveComplaints(data) {
    localStorage.setItem(DB_KEY, JSON.stringify(data));
}

function addComplaint(complaint) {
    const data = getComplaints();
    // Generate new ID
    const newId = data.length > 0 ? Math.max(...data.map(c => c.id)) + 1 : 101;
    complaint.id = newId;
    complaint.created_at = new Date().toISOString().slice(0, 19).replace('T', ' ');
    complaint.status = 'Pending';

    // Add to top
    data.unshift(complaint);
    saveComplaints(data);
    return newId;
}

function updateComplaintStatus(id, newStatus, remark) {
    const data = getComplaints();
    const idx = data.findIndex(c => c.id == id);
    if (idx !== -1) {
        data[idx].status = newStatus;
        if (remark) data[idx].admin_remark = remark;
        saveComplaints(data);
        return true;
    }
    return false;
}

function getStats() {
    const data = getComplaints();
    return {
        total: data.length,
        pending: data.filter(c => c.status === 'Pending').length,
        resolved: data.filter(c => c.status === 'Resolved').length
    };
}
