/**
 * Order table manager
 */
class OrderTableManager {
    static init() {
        this.fetchAndDisplayOrders();
        this.setupEventHandlers();
    }

    static fetchAndDisplayOrders() {
        fetch('/api/orders')
            .then(r => r.json())
            .then(response => {
                const data = response.data || response;
                const orders = data.items || [];
                
                this.displayOrderStats(orders);
                this.setupDataTable(orders);
            })
            .catch(error => {
                console.error('Error loading orders:', error);
                Utils.showToast('Failed to load orders', 'error');
            });
    }

    static displayOrderStats(orders) {
        const thisMonth = new Date().getMonth();
        const thisMonthOrders = orders.filter(o => new Date(o.created_at).getMonth() === thisMonth);
        
        const statsInfo = document.getElementById('statsInfo');
        if (statsInfo) {
            statsInfo.innerHTML = `
                <p><strong>Total Orders:</strong> ${orders.length}</p>
                <p><strong>This Month:</strong> ${thisMonthOrders.length}</p>
                <p><strong>Pending:</strong> ${orders.filter(o => o.status === 'pending').length}</p>
                <p><strong>Completed:</strong> ${orders.filter(o => o.status === 'completed').length}</p>
            `;
        }
    }

    static setupDataTable(orders) {
        const table = new DataTable('ordersTable', [
            {key: 'id', label: 'ID', render: v => `#${v}`},
            {key: 'bw_quantity', label: 'B&W', render: (v, row) => row.bw_quantity || row.bw_count || 0},
            {key: 'color_quantity', label: 'Color', render: (v, row) => row.color_quantity || row.color_count || 0},
            {key: 'status', label: 'Status', render: v => `<span class="badge bg-${
                v === 'completed' ? 'success' : 
                v === 'processing' ? 'primary' : 
                v === 'validated' ? 'info' : 'warning'
            }">${v}</span>`},
            {key: 'created_at', label: 'Created', render: v => Utils.formatDate(v)}
        ], {
            actions: [
                {
                    icon: 'eye',
                    label: 'View Details',
                    onClick: order => viewOrderDetails(order.id),
                    className: 'btn-outline-primary'
                }
            ]
        });

        table.setData(orders);
    }

    static setupEventHandlers() {
        // Add any additional event handlers here
        const createOrderForm = document.getElementById('createOrderForm');
        if (createOrderForm) {
            createOrderForm.addEventListener('submit', this.handleOrderSubmit.bind(this));
        }
    }

    static async handleOrderSubmit(e) {
        e.preventDefault();
        
        const bwCount = parseInt(document.getElementById('bwCount').value) || 0;
        const colorCount = parseInt(document.getElementById('colorCount').value) || 0;
        
        if (bwCount === 0 && colorCount === 0) {
            Utils.showToast('Please specify at least one print quantity (B&W or Color)', 'error');
            return;
        }
        
        const formData = {
            bw_quantity: bwCount,
            color_quantity: colorCount,
            paper_dimensions: document.getElementById('paperDimensions').value || null,
            notes: document.getElementById('additionalOptions').value || null
        };
        
        const btn = document.getElementById('createOrderBtn');
        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = 'Creating...';
        
        try {
            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                Utils.showToast('Order created successfully!', 'success');
                e.target.reset();
                location.reload();
            } else {
                Utils.showToast(result.message || 'Failed to create order', 'error');
            }
        } catch (err) {
            console.error('Order creation error:', err);
            Utils.showToast('Network error. Please try again.', 'error');
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    }
}

// Initialize order table manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('ordersTable')) {
        OrderTableManager.init();
    }
});