/**
 * Reusable UI Components for VersatilesPrint
 * Generic modals, tables, and utilities
 */

// ============================================================================
// MODAL UTILITIES
// ============================================================================

class ModalManager {
    /**
     * Show loading overlay
     */
    static showLoading(message = 'Please wait...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = document.getElementById('loadingText');
        if (text) text.textContent = message;
        if (overlay) overlay.classList.remove('d-none');
    }

    /**
     * Hide loading overlay
     */
    static hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) overlay.classList.add('d-none');
    }

    /**
     * Show error in modal
     */
    static showError(modalId, errorElementId, message) {
        const errorEl = document.getElementById(errorElementId);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.classList.remove('d-none');
        }
    }

    /**
     * Hide error in modal
     */
    static hideError(errorElementId) {
        const errorEl = document.getElementById(errorElementId);
        if (errorEl) {
            errorEl.classList.add('d-none');
        }
    }

    /**
     * Close modal by ID
     */
    static closeModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) modal.hide();
    }

    /**
     * Open modal by ID
     */
    static openModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    /**
     * Generic delete confirmation
     */
    static confirmDelete(itemName, onConfirm, warningText = 'This action cannot be undone.') {
        const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
        document.getElementById('deleteConfirmMessage').textContent = 
            `Are you sure you want to delete "${itemName}"?`;
        document.getElementById('deleteWarningText').textContent = warningText;
        
        const confirmBtn = document.getElementById('confirmDeleteBtn');
        // Remove old listeners
        const newBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
        
        // Add new listener
        document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
            onConfirm();
        });
        
        modal.show();
    }
}

// ============================================================================
// TABLE MANAGER
// ============================================================================

class DataTable {
    constructor(containerId, columns, options = {}) {
        this.containerId = containerId;
        this.columns = columns; // [{key, label, render?, sortable?, width?}]
        this.options = {
            actions: options.actions || [], // [{icon, label, onClick, className, condition?}]
            searchable: options.searchable !== false,
            sortable: options.sortable !== false,
            pagination: options.pagination !== false,
            pageSize: options.pageSize || 20,
            emptyMessage: options.emptyMessage || 'No data available',
            tableClass: options.tableClass || 'table table-hover table-striped',
            onRowClick: options.onRowClick || null
        };
        this.data = [];
        this.filteredData = [];
        this.currentPage = 1;
        this.sortColumn = null;
        this.sortDirection = 'asc';
    }

    /**
     * Set data and render table
     */
    setData(data) {
        this.data = data;
        this.filteredData = [...data];
        this.currentPage = 1;
        this.render();
    }

    /**
     * Search/filter data
     */
    search(query) {
        if (!query) {
            this.filteredData = [...this.data];
        } else {
            query = query.toLowerCase();
            this.filteredData = this.data.filter(row => {
                return this.columns.some(col => {
                    const value = row[col.key];
                    return value && value.toString().toLowerCase().includes(query);
                });
            });
        }
        this.currentPage = 1;
        this.render();
    }

    /**
     * Sort data
     */
    sort(columnKey) {
        if (this.sortColumn === columnKey) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = columnKey;
            this.sortDirection = 'asc';
        }

        this.filteredData.sort((a, b) => {
            let aVal = a[columnKey];
            let bVal = b[columnKey];
            
            if (aVal === null || aVal === undefined) return 1;
            if (bVal === null || bVal === undefined) return -1;
            
            if (typeof aVal === 'string') aVal = aVal.toLowerCase();
            if (typeof bVal === 'string') bVal = bVal.toLowerCase();
            
            if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
            if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
            return 0;
        });

        this.render();
    }

    /**
     * Go to page
     */
    goToPage(page) {
        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        if (page < 1 || page > totalPages) return;
        this.currentPage = page;
        this.render();
    }

    /**
     * Render table
     */
    render() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        // Calculate pagination
        const totalItems = this.filteredData.length;
        const totalPages = Math.ceil(totalItems / this.options.pageSize);
        const start = (this.currentPage - 1) * this.options.pageSize;
        const end = Math.min(start + this.options.pageSize, totalItems);
        const pageData = this.filteredData.slice(start, end);

        // Build HTML
        let html = '<div class="table-responsive">';
        
        // Table
        html += `<table class="${this.options.tableClass}">`;
        
        // Header
        html += '<thead class="table-dark"><tr>';
        this.columns.forEach(col => {
            const sortIcon = this.sortColumn === col.key ? 
                (this.sortDirection === 'asc' ? '▲' : '▼') : '';
            const sortable = col.sortable !== false && this.options.sortable;
            html += `<th ${col.width ? `style="width:${col.width}"` : ''} 
                     ${sortable ? `style="cursor:pointer" onclick="window.dataTable_${this.containerId}.sort('${col.key}')"` : ''}>
                     ${col.label} ${sortIcon}
                     </th>`;
        });
        if (this.options.actions.length > 0) {
            html += '<th style="width:150px">Actions</th>';
        }
        html += '</tr></thead>';

        // Body
        html += '<tbody>';
        if (pageData.length === 0) {
            html += `<tr><td colspan="${this.columns.length + (this.options.actions.length > 0 ? 1 : 0)}" class="text-center text-muted py-4">
                     ${this.options.emptyMessage}</td></tr>`;
        } else {
            pageData.forEach((row, idx) => {
                const rowClass = this.options.onRowClick ? 'cursor-pointer' : '';
                const rowClick = this.options.onRowClick ? 
                    `onclick="(${this.options.onRowClick.toString()})(${JSON.stringify(row).replace(/"/g, '&quot;')})"` : '';
                html += `<tr class="${rowClass}" ${rowClick}>`;
                
                this.columns.forEach(col => {
                    const value = row[col.key];
                    const rendered = col.render ? col.render(value, row) : (value || '');
                    html += `<td>${rendered}</td>`;
                });

                if (this.options.actions.length > 0) {
                    html += '<td><div class="btn-group btn-group-sm" role="group">';
                    this.options.actions.forEach(action => {
                        // Check condition
                        if (action.condition && !action.condition(row)) return;
                        
                        const className = action.className || 'btn-outline-primary';
                        const disabled = action.disabled && action.disabled(row) ? 'disabled' : '';
                        html += `<button class="btn ${className}" ${disabled} 
                                 onclick="(${action.onClick.toString()})(${JSON.stringify(row).replace(/"/g, '&quot;')})" 
                                 title="${action.label}">
                                 <i class="bi bi-${action.icon}"></i>
                                 </button>`;
                    });
                    html += '</div></td>';
                }
                
                html += '</tr>';
            });
        }
        html += '</tbody>';
        html += '</table>';
        html += '</div>';

        // Pagination
        if (this.options.pagination && totalPages > 1) {
            html += '<nav><ul class="pagination justify-content-center">';
            
            // Previous
            html += `<li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                     <a class="page-link" onclick="window.dataTable_${this.containerId}.goToPage(${this.currentPage - 1})">Previous</a>
                     </li>`;
            
            // Pages
            for (let i = 1; i <= totalPages; i++) {
                if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                    html += `<li class="page-item ${i === this.currentPage ? 'active' : ''}">
                             <a class="page-link" onclick="window.dataTable_${this.containerId}.goToPage(${i})">${i}</a>
                             </li>`;
                } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
                    html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
                }
            }
            
            // Next
            html += `<li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                     <a class="page-link" onclick="window.dataTable_${this.containerId}.goToPage(${this.currentPage + 1})">Next</a>
                     </li>`;
            
            html += '</ul></nav>';
            
            // Info
            html += `<p class="text-center text-muted">
                     Showing ${start + 1} to ${end} of ${totalItems} entries
                     </p>`;
        }

        container.innerHTML = html;
        
        // Store reference globally for onclick handlers
        window[`dataTable_${this.containerId}`] = this;
    }
}

// ============================================================================
// API UTILITIES
// ============================================================================

class API {
    /**
     * Generic fetch wrapper
     */
    static async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error?.message || data.message || 'Request failed');
            }

            return {success: true, data: data.data || data, message: data.message};
        } catch (error) {
            return {success: false, error: error.message};
        }
    }

    static async get(url) {
        return this.request(url, {method: 'GET'});
    }

    static async post(url, body) {
        return this.request(url, {method: 'POST', body: JSON.stringify(body)});
    }

    static async patch(url, body) {
        return this.request(url, {method: 'PATCH', body: JSON.stringify(body)});
    }

    static async delete(url) {
        return this.request(url, {method: 'DELETE'});
    }
}

// ============================================================================
// HELPER UTILITIES
// ============================================================================

class Utils {
    /**
     * Format date
     */
    static formatDate(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString();
    }

    /**
     * Format datetime
     */
    static formatDateTime(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleString();
    }

    /**
     * Create badge HTML
     */
    static badge(text, className = 'secondary') {
        return `<span class="badge bg-${className}">${text}</span>`;
    }

    /**
     * Show toast notification
     */
    static showToast(message, type = 'success') {
        const container = document.getElementById('toastContainer');
        if (!container) {
            console.warn('Toast container not found. Using alert as fallback.');
            alert((type === 'success' ? '✓ ' : '✗ ') + message);
            return;
        }

        // Generate unique ID for this toast
        const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        // Icon and color mapping
        const iconMap = {
            success: 'check-circle-fill',
            error: 'x-circle-fill',
            warning: 'exclamation-triangle-fill',
            info: 'info-circle-fill'
        };
        
        const colorMap = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#118843'
        };
        
        const icon = iconMap[type] || iconMap.info;
        const color = colorMap[type] || colorMap.info;
        
        // Create toast HTML
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center">
                        <i class="bi bi-${icon} me-2" style="color: ${color}; font-size: 1.2rem;"></i>
                        <span>${message}</span>
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;
        
        // Append to container
        container.insertAdjacentHTML('beforeend', toastHtml);
        
        // Initialize and show the toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: type === 'error' ? 5000 : 3000
        });
        
        toast.show();
        
        // Remove from DOM after hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
    
    /**
     * Legacy alias for showToast
     */
    static toast(message, type = 'success') {
        return this.showToast(message, type);
    }
}

// Export for global use
window.ModalManager = ModalManager;
window.DataTable = DataTable;
window.API = API;
window.Utils = Utils;
