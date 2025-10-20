// VersatilesPrint - Main Application JavaScript

// Utility Functions
const showLoading = (text = 'Please wait...') => {
    document.getElementById('loadingText').textContent = text;
    document.getElementById('loadingOverlay').classList.remove('d-none');
};

const hideLoading = () => {
    document.getElementById('loadingOverlay').classList.add('d-none');
};

const showError = (elementId, message) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.remove('d-none');
    }
};

const hideError = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('d-none');
    }
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

// User Management
let currentUserId = null;

const openUserModal = (userId = null) => {
    currentUserId = userId;
    hideError('userModalError');
    
    if (userId) {
        // Edit mode
        document.getElementById('userModalTitle').textContent = 'Edit User';
        document.getElementById('passwordField').classList.add('d-none');
        document.getElementById('userPassword').required = false;
        
        // Load user data
        showLoading('Loading user data...');
        fetch(`/api/users/${userId}`)
            .then(r => r.json())
            .then(data => {
                hideLoading();
                if (data.data) {
                    document.getElementById('userId').value = data.data.id;
                    document.getElementById('userEmail').value = data.data.email;
                    document.getElementById('userEmail').disabled = true;
                    document.getElementById('userFullName').value = data.data.full_name || '';
                    document.getElementById('userRole').value = data.data.role_name;
                    document.getElementById('userActive').checked = data.data.is_active;
                }
            })
            .catch(() => {
                hideLoading();
                showError('userModalError', 'Failed to load user data');
            });
    } else {
        // Create mode
        document.getElementById('userModalTitle').textContent = 'Create New User';
        document.getElementById('passwordField').classList.remove('d-none');
        document.getElementById('userPassword').required = true;
        document.getElementById('userForm').reset();
        document.getElementById('userEmail').disabled = false;
    }
    
    new bootstrap.Modal(document.getElementById('userModal')).show();
};

const saveUser = async () => {
    hideError('userModalError');
    
    const email = document.getElementById('userEmail').value.trim();
    const fullName = document.getElementById('userFullName').value.trim();
    const role = document.getElementById('userRole').value;
    const isActive = document.getElementById('userActive').checked;
    
    // Client-side validation
    if (!email) {
        showError('userModalError', 'Email is required');
        return;
    }
    
    if (!role) {
        showError('userModalError', 'Please select a role');
        return;
    }
    
    const formData = {
        email: email,
        full_name: fullName,
        role: role,
        is_active: isActive
    };
    
    if (!currentUserId) {
        const password = document.getElementById('userPassword').value;
        if (!password) {
            showError('userModalError', 'Password is required');
            return;
        }
        formData.password = password;
    }
    
    const url = currentUserId ? `/api/users/${currentUserId}` : '/api/users';
    const method = currentUserId ? 'PATCH' : 'POST';
    
    try {
        showLoading('Saving user...');
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            location.reload();
        } else {
            showError('userModalError', data.message || 'Failed to save user');
        }
    } catch (error) {
        hideLoading();
        console.error('Error saving user:', error);
        showError('userModalError', 'Network error. Please try again.');
    }
};

// CSV Import
let currentImportId = null;

const openCsvModal = () => {
    document.getElementById('csvUploadSection').classList.remove('d-none');
    document.getElementById('csvPreviewSection').classList.add('d-none');
    document.getElementById('uploadCsvBtn').classList.remove('d-none');
    document.getElementById('validateCsvBtn').classList.add('d-none');
    document.getElementById('csvFile').value = '';
    hideError('csvUploadError');
    
    new bootstrap.Modal(document.getElementById('csvModal')).show();
};

const uploadCsv = async () => {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('csvUploadError', 'Please select a CSV file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showLoading('Uploading CSV file...');
        const response = await fetch('/api/csv-imports', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok) {
            currentImportId = data.data.id;
            loadCsvPreview(currentImportId);
        } else {
            showError('csvUploadError', data.message || 'Upload failed');
        }
    } catch (error) {
        hideLoading();
        showError('csvUploadError', 'Network error. Please try again.');
    }
};

const loadCsvPreview = async (importId) => {
    showLoading('Validating CSV...');
    
    try {
        const response = await fetch(`/api/csv-imports/${importId}`);
        const data = await response.json();
        hideLoading();
        
        if (response.ok && data.data) {
            displayCsvPreview(data.data);
        } else {
            showError('csvUploadError', data.message || 'Failed to load preview');
        }
    } catch (error) {
        hideLoading();
        showError('csvUploadError', 'Network error. Please try again.');
    }
};

const displayCsvPreview = (data) => {
    const validation = data.validation;
    const previewContent = document.getElementById('csvPreviewContent');
    
    let html = `
        <div class="alert alert-${validation.is_valid ? 'success' : 'warning'}">
            <strong>Validation Results:</strong><br>
            Total Rows: ${validation.total_rows}<br>
            Valid Rows: ${validation.valid_rows}<br>
            Invalid Rows: ${validation.errors.length}
        </div>
    `;
    
    if (validation.errors.length > 0) {
        html += '<div class="alert alert-danger"><strong>Errors:</strong><ul class="mb-0">';
        validation.errors.slice(0, 10).forEach(error => {
            html += `<li>Row ${error.row}: ${error.message}</li>`;
        });
        if (validation.errors.length > 10) {
            html += `<li>... and ${validation.errors.length - 10} more errors</li>`;
        }
        html += '</ul></div>';
    }
    
    previewContent.innerHTML = html;
    document.getElementById('csvUploadSection').classList.add('d-none');
    document.getElementById('csvPreviewSection').classList.remove('d-none');
    document.getElementById('uploadCsvBtn').classList.add('d-none');
    document.getElementById('validateCsvBtn').classList.remove('d-none');
};

const validateCsv = async () => {
    if (!currentImportId) return;
    
    try {
        showLoading('Importing data...');
        const response = await fetch(`/api/csv-imports/${currentImportId}/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ corrections: {} })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('csvModal')).hide();
            alert(`Import successful! Created ${data.data.created_count} users and ${data.data.created_orders} orders.`);
            location.reload();
        } else {
            showError('csvUploadError', data.message || 'Import failed');
        }
    } catch (error) {
        hideLoading();
        alert('Network error. Please try again.');
    }
};

// Order Details
const viewOrderDetails = async (orderId) => {
    const modal = new bootstrap.Modal(document.getElementById('orderModal'));
    modal.show();
    
    try {
        const response = await fetch(`/api/orders/${orderId}`);
        const data = await response.json();
        
        if (response.ok && data.data) {
            displayOrderDetails(data.data);
        } else {
            document.getElementById('orderModalBody').innerHTML = 
                '<div class="alert alert-danger">Failed to load order details</div>';
        }
    } catch (error) {
        document.getElementById('orderModalBody').innerHTML = 
            '<div class="alert alert-danger">Network error. Please try again.</div>';
    }
};

const displayOrderDetails = (order) => {
    const statusColors = {
        'pending': 'warning',
        'validated': 'info',
        'processing': 'primary',
        'completed': 'success',
        'cancelled': 'danger'
    };
    
    const html = `
        <div class="row">
            <div class="col-md-6">
                <p><strong>Order ID:</strong> #${order.id}</p>
                <p><strong>Status:</strong> <span class="badge bg-${statusColors[order.status]}">${order.status}</span></p>
                <p><strong>Client:</strong> ${order.client_email || 'N/A'}</p>
                <p><strong>Agent:</strong> ${order.agent_email || 'Unassigned'}</p>
            </div>
            <div class="col-md-6">
                <p><strong>B&W Prints:</strong> ${order.bw_count}</p>
                <p><strong>Color Prints:</strong> ${order.color_count}</p>
                <p><strong>Paper Size:</strong> ${order.paper_dimensions || 'N/A'}</p>
                <p><strong>Orientation:</strong> ${order.orientation || 'N/A'}</p>
            </div>
        </div>
        ${order.additional_options ? `
            <div class="mt-3">
                <strong>Additional Options:</strong>
                <p class="text-muted">${order.additional_options}</p>
            </div>
        ` : ''}
        <div class="mt-3">
            <p><strong>Created:</strong> ${formatDate(order.created_at)}</p>
            ${order.updated_at ? `<p><strong>Updated:</strong> ${formatDate(order.updated_at)}</p>` : ''}
        </div>
    `;
    
    document.getElementById('orderModalBody').innerHTML = html;
};

// Quota Top-up
const openTopupModal = () => {
    hideError('topupError');
    document.getElementById('topupForm').reset();
    
    // Load clients
    fetch('/api/users?role=Client')
        .then(r => r.json())
        .then(data => {
            const select = document.getElementById('topupClient');
            select.innerHTML = '<option value="">Select a client...</option>';
            if (data.items) {
                data.items.forEach(client => {
                    select.innerHTML += `<option value="${client.id}">${client.full_name || client.email}</option>`;
                });
            }
        });
    
    new bootstrap.Modal(document.getElementById('topupModal')).show();
};

const saveTopup = async () => {
    hideError('topupError');
    
    const clientId = document.getElementById('topupClient').value;
    const bwAmount = parseInt(document.getElementById('topupBw').value) || 0;
    const colorAmount = parseInt(document.getElementById('topupColor').value) || 0;
    const notes = document.getElementById('topupNotes').value;
    
    if (!clientId) {
        showError('topupError', 'Please select a client');
        return;
    }
    
    if (bwAmount === 0 && colorAmount === 0) {
        showError('topupError', 'Please specify at least one type of top-up');
        return;
    }
    
    const formData = {
        client_id: parseInt(clientId),
        bw_amount: bwAmount,
        color_amount: colorAmount,
        notes: notes
    };
    
    try {
        showLoading('Adding top-up...');
        const response = await fetch('/api/quotas/topup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('topupModal')).hide();
            alert('Quota top-up added successfully!');
            location.reload();
        } else {
            showError('topupError', data.message || 'Failed to add top-up');
        }
    } catch (error) {
        hideLoading();
        showError('topupError', 'Network error. Please try again.');
    }
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // User Modal
    const saveUserBtn = document.getElementById('saveUserBtn');
    if (saveUserBtn) {
        saveUserBtn.addEventListener('click', saveUser);
    }
    
    // CSV Modal
    const uploadCsvBtn = document.getElementById('uploadCsvBtn');
    if (uploadCsvBtn) {
        uploadCsvBtn.addEventListener('click', uploadCsv);
    }
    
    const validateCsvBtn = document.getElementById('validateCsvBtn');
    if (validateCsvBtn) {
        validateCsvBtn.addEventListener('click', validateCsv);
    }
    
    // Topup Modal
    const saveTopupBtn = document.getElementById('saveTopupBtn');
    if (saveTopupBtn) {
        saveTopupBtn.addEventListener('click', saveTopup);
    }
});

// Make functions globally available
window.openUserModal = openUserModal;
window.openCsvModal = openCsvModal;
window.viewOrderDetails = viewOrderDetails;
window.openTopupModal = openTopupModal;
