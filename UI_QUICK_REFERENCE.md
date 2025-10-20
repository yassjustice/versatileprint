# VersatilesPrint UI - Quick Reference

## 🎯 Dashboard Overview

### **Client View** - For printing customers
```
┌─────────────────────────────────────────────────┐
│ Dashboard - Welcome, Client Name                │
├─────────────────┬───────────────────────────────┤
│  My Quota       │  Quick Stats                  │
│  B&W: 150/3000  │  Total Orders: 25             │
│  [████░░░] 5%   │  This Month: 3                │
│  Color: 100/2000│  Pending: 1                   │
│  [███░░░] 5%    │  Completed: 20                │
└─────────────────┴───────────────────────────────┘
│  Create New Order Form                          │
│  [B&W] [Color] [Paper] [Submit]                 │
└─────────────────────────────────────────────────┘
│  My Orders Table                                │
│  ID  │ B&W │ Color │ Status │ Date │ Actions   │
└─────────────────────────────────────────────────┘
```

### **Agent View** - For order processors
```
┌─────────────────────────────────────────────────┐
│ Dashboard - Welcome, Agent Name                 │
├─────────────┬─────────────┬─────────────────────┤
│ Active: 7   │ Completed:20│ Capacity: 7/10      │
└─────────────┴─────────────┴─────────────────────┘
│  Assigned Orders Table                          │
│  ID │ Client │ B&W │ Color │ Status │ Actions  │
└─────────────────────────────────────────────────┘
```

### **Administrator View** - For system management
```
┌─────────────────────────────────────────────────┐
│ Dashboard - Welcome, Admin Name                 │
├───────────┬───────────┬───────────┬─────────────┤
│ Users: 15 │ Orders:50 │ CSV: 2    │ Clients: 10 │
└───────────┴───────────┴───────────┴─────────────┘
│ [Orders] [Users] [CSV Imports]                  │
├─────────────────────────────────────────────────┤
│  All Orders / Users / CSV Imports               │
│  [Add New User] [Upload CSV] [Add Top-up]       │
│  ┌───────────────────────────────────────────┐  │
│  │ Table with full data and actions          │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 📊 API Endpoints Used

| Endpoint | Method | Used By | Purpose |
|----------|--------|---------|---------|
| `/api/quotas` | GET | Client | Get client's quota info |
| `/api/orders` | GET | All | Get orders (filtered by role) |
| `/api/orders` | POST | Client | Create new order |
| `/api/orders/:id` | GET | All | Get order details |
| `/api/users` | GET | Admin | List all users |
| `/api/users` | POST | Admin | Create new user |
| `/api/users/:id` | GET | Admin | Get user details |
| `/api/users/:id` | PATCH | Admin | Update user |
| `/api/csv-imports` | GET | Admin | List CSV imports |
| `/api/csv-imports` | POST | Admin | Upload CSV |
| `/api/csv-imports/:id` | GET | Admin | Get import details |
| `/api/csv-imports/:id/validate` | POST | Admin | Validate CSV |
| `/api/quotas/topup` | POST | Admin | Add quota top-up |
| `/api/notifications` | GET | All | Get notifications |

---

## 🎨 UI Components

### **Modals**
1. **User Modal** - Create/Edit users (Admin only)
2. **CSV Modal** - Upload and validate CSV files (Admin only)
3. **Order Modal** - View order details (All roles)
4. **Top-up Modal** - Add quota top-up (Admin only)

### **Status Badges**

#### Orders
- `pending` → 🟡 Yellow
- `validated` → 🔵 Blue
- `processing` → 🔵 Primary
- `completed` → 🟢 Green
- `cancelled` → 🔴 Red

#### CSV Imports
- `pending_validation` → 🟡 Yellow
- `validated` → 🟢 Green
- `rejected` → 🔴 Red

#### User Roles
- `Administrator` → 🔴 Red
- `Agent` → 🔵 Blue
- `Client` → 🟢 Green

#### User Status
- `Active` → 🟢 Green
- `Inactive` → ⚪ Gray

---

## 🔄 Data Refresh

| Action | Refresh Method |
|--------|---------------|
| Create Order | `location.reload()` |
| Create User | `location.reload()` |
| Upload CSV | `location.reload()` |
| Add Top-up | `location.reload()` |
| Update User | `location.reload()` |

**Manual Refresh:** Press `Ctrl + R` or `F5`

---

## 🎯 Key Functions (JavaScript)

```javascript
// Modal Functions
openUserModal(userId?)         // Open user create/edit modal
openCsvModal()                 // Open CSV upload modal
openTopupModal()               // Open quota top-up modal

// Display Functions
viewOrderDetails(orderId)      // Show order details modal
reviewCsvImport(importId)      // Review pending CSV import
viewCsvDetails(importId)       // View CSV import details

// Form Functions
saveUser()                     // Save user (create/update)
uploadCsv()                    // Upload CSV file
validateCsv()                  // Validate and import CSV
saveTopup()                    // Add quota top-up

// Utility Functions
showLoading(text)              // Show loading overlay
hideLoading()                  // Hide loading overlay
showError(elementId, message)  // Show error message
hideError(elementId)           // Hide error message
formatDate(dateString)         // Format date for display
```

---

## 📋 Field Mappings

### Order Object
```javascript
{
    id: 1,
    client_id: 2,
    agent_id: 3,
    status: "pending",
    bw_quantity: 100,        // ← Use this
    color_quantity: 50,      // ← Use this
    paper_dimensions: "A4",
    paper_type: "matte",
    finishing: "staple",
    created_at: "2025-10-20T10:00:00",
    updated_at: "2025-10-20T11:00:00",
    notes: "Special instructions",
    external_order_id: "EXT123",
    client_email: "client@example.com",  // ← Direct access
    agent_email: "agent@example.com"     // ← Direct access
}
```

### User Object
```javascript
{
    id: 1,
    email: "user@example.com",
    full_name: "John Doe",
    is_active: true,
    created_at: "2025-01-01T00:00:00",
    last_login: "2025-10-20T10:00:00",
    role: {
        id: 1,
        name: "Client"
    },
    role_name: "Client"  // ← Convenience field
}
```

### CSV Import Object
```javascript
{
    id: 1,
    original_filename: "orders.csv",
    status: "pending_validation",
    uploaded_at: "2025-10-20T10:00:00",
    validated_at: null,
    row_count: 50,
    valid_rows: 48,
    error_rows: 2,
    notes: "Admin review notes",
    uploaded_by_email: "admin@example.com",  // ← Direct access
    validated_by_email: null
}
```

### Quota Object
```javascript
{
    id: 1,
    client_id: 2,
    month: "2025-10-01",
    bw_limit: 3000,
    color_limit: 2000,
    bw_used: 150,
    color_used: 100,
    bw_available: 2850,
    color_available: 1900,
    bw_alert_sent: false,
    color_alert_sent: false
}
```

---

## 🎨 CSS Classes

### Bootstrap Components
```css
.card                  /* Container cards */
.table-hover           /* Interactive tables */
.badge                 /* Status indicators */
.progress              /* Progress bars */
.modal                 /* Modal dialogs */
.btn                   /* Buttons */
.alert                 /* Messages */
```

### Custom Classes
```css
.clickable             /* Cursor pointer for rows */
.loading-overlay       /* Full-screen loading */
.loading-spinner       /* Loading animation */
```

---

## 🔍 Debugging

### Browser Console
```javascript
// Check if functions are loaded
typeof openUserModal           // Should be "function"
typeof viewOrderDetails        // Should be "function"

// Test API manually
fetch('/api/orders').then(r => r.json()).then(console.log)
fetch('/api/users').then(r => r.json()).then(console.log)
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Functions undefined | Hard refresh (Ctrl + Shift + R) |
| Data not loading | Check browser console for errors |
| 400/500 errors | Check Flask terminal logs |
| Empty tables | Verify API returns data |
| Modal not opening | Check Bootstrap is loaded |

---

## 📱 Responsive Breakpoints

- **Desktop:** > 992px (Full tables, side-by-side cards)
- **Tablet:** 768px - 991px (Responsive tables)
- **Mobile:** < 768px (Stacked cards, horizontal scroll tables)

---

## ⚡ Performance Tips

1. **Minimize API calls** - Data loaded once on page load
2. **Use pagination** - For large datasets
3. **Cache in browser** - Until page reload
4. **Lazy load modals** - Only fetch details when opened
5. **Parallel requests** - Use `Promise.all()` for admin dashboard

---

## 🔒 Security Notes

- All endpoints require authentication (`@login_required`)
- Admin functions require admin role (`@admin_required`)
- CSRF protection enabled for forms
- Password requirements enforced
- SQL injection protection via SQLAlchemy ORM

---

## 📞 Quick Actions

### As Client:
- **Create Order:** Fill form → Click "Create Order"
- **View Order:** Click order row or "View" button

### As Agent:
- **View Order:** Click order row or "View" button
- **Process Orders:** (Future feature)

### As Admin:
- **Add User:** Click "Add New User" → Fill form → Save
- **Edit User:** Click "Edit" → Modify → Save
- **Upload CSV:** Click "Upload CSV" → Select file → Upload → Validate
- **Add Top-up:** Click "Add Quota Top-up" → Select client → Enter amounts → Save
- **Review CSV:** Click "Review" on pending imports

---

**Quick Tip:** Press `F12` to open Developer Tools for debugging!
