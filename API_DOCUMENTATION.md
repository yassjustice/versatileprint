# VersatilesPrint API Documentation

## Base URL
```
http://localhost:5000/api
```

All API responses follow a standard JSON format.

## Authentication

All API endpoints (except `/auth/login`) require authentication. Use session-based authentication via cookies.

---

## Authentication Endpoints

### POST /api/auth/login
Login to the system.

**Request Body:**
```json
{
  "email": "admin@versatiles.com",
  "password": "Admin123!",
  "remember": false
}
```

**Response (200):**
```json
{
  "data": {
    "user": {
      "id": 1,
      "email": "admin@versatiles.com",
      "full_name": "System Administrator",
      "is_active": true,
      "role": {
        "id": 3,
        "name": "Administrator"
      }
    },
    "message": "Login successful"
  }
}
```

### POST /api/auth/logout
Logout current user.

**Response (204):**
No content

### GET /api/auth/me
Get current authenticated user.

**Response (200):**
```json
{
  "data": {
    "id": 1,
    "email": "admin@versatiles.com",
    "full_name": "System Administrator",
    "is_active": true,
    "role": {
      "id": 3,
      "name": "Administrator"
    }
  }
}
```

---

## User Management (Admin Only)

### GET /api/users
List all users with optional filters.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20)
- `role` (string): Filter by role (Client, Agent, Administrator)
- `is_active` (boolean): Filter by active status

**Response (200):**
```json
{
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 50,
      "total_pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### POST /api/users
Create a new user.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "full_name": "New User",
  "role": "Client"
}
```

**Response (201):**
```json
{
  "data": {
    "id": 10,
    "email": "newuser@example.com",
    "full_name": "New User",
    "is_active": true,
    "role": {
      "id": 1,
      "name": "Client"
    }
  },
  "message": "User created successfully"
}
```

### GET /api/users/:id
Get user details.

### PATCH /api/users/:id
Update user details.

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "is_active": true,
  "role": "Agent"
}
```

### POST /api/users/:id/reset-password
Reset user password (Admin only).

**Request Body:**
```json
{
  "new_password": "NewSecurePass123!"
}
```

---

## Orders

### GET /api/orders
List orders (role-filtered).

**Query Parameters:**
- `page` (int): Page number
- `page_size` (int): Items per page
- `status` (string): Filter by status (pending, validated, processing, completed)

**Response (200):**
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "client_id": 2,
        "agent_id": 3,
        "status": "pending",
        "bw_quantity": 100,
        "color_quantity": 50,
        "paper_dimensions": "A4",
        "paper_type": "matte",
        "finishing": "none",
        "created_at": "2025-10-14T10:30:00",
        "notes": "Standard order"
      }
    ],
    "pagination": {...}
  }
}
```

### POST /api/orders
Create a new order.

**Request Body (Client):**
```json
{
  "bw_quantity": 100,
  "color_quantity": 50,
  "paper_dimensions": "A4",
  "paper_type": "matte",
  "finishing": "none",
  "notes": "My order"
}
```

**Request Body (Agent creating for client):**
```json
{
  "client_id": 5,
  "bw_quantity": 100,
  "color_quantity": 50,
  "paper_dimensions": "A4",
  "paper_type": "matte",
  "finishing": "staple"
}
```

**Response (201):**
```json
{
  "data": {
    "id": 15,
    "client_id": 2,
    "status": "pending",
    "bw_quantity": 100,
    "color_quantity": 50,
    ...
  },
  "message": "Order created"
}
```

**Error Response (400 - Quota Exceeded):**
```json
{
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "Insufficient B&W quota. Available: 250/3000 (91.7% used). Requested: 500. Please reduce quantity or request a top-up."
  }
}
```

### GET /api/orders/:id
Get order details (with authorization check).

### POST /api/orders/:id/status
Change order status (Admin only).

**Request Body:**
```json
{
  "status": "validated"
}
```

**Allowed Transitions:**
- pending → validated
- validated → processing
- processing → completed

---

## Quotas

### GET /api/quotas
Get quota information.

**Query Parameters:**
- `client_id` (int): Client ID (required for Admin/Agent, auto-filled for Client)
- `month` (string): Month in YYYY-MM format (optional, defaults to current month)

**Response (200):**
```json
{
  "data": {
    "client_id": 2,
    "month": "2025-10-01",
    "bw": {
      "base_limit": 3000,
      "topups": 1000,
      "total_limit": 4000,
      "used": 2500,
      "available": 1500,
      "percentage_used": 62.5
    },
    "color": {
      "base_limit": 2000,
      "topups": 0,
      "total_limit": 2000,
      "used": 1800,
      "available": 200,
      "percentage_used": 90.0
    },
    "topups_history": [...]
  }
}
```

### POST /api/quotas/topup
Create quota top-up (Admin only).

**Request Body:**
```json
{
  "client_id": 2,
  "bw_added": 1000,
  "color_added": 1000,
  "notes": "Monthly top-up request"
}
```

**Response (201):**
```json
{
  "data": {
    "id": 5,
    "client_id": 2,
    "admin_id": 1,
    "bw_added": 1000,
    "color_added": 1000,
    "transaction_date": "2025-10-14T15:30:00",
    "notes": "Monthly top-up request"
  },
  "message": "Top-up created"
}
```

---

## CSV Imports (Admin Only)

### GET /api/csv-imports
List all CSV imports.

### POST /api/csv-imports
Upload CSV file.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (CSV file)

**Response (201):**
```json
{
  "data": {
    "id": 3,
    "original_filename": "orders_batch_1.csv",
    "status": "pending_validation",
    "uploaded_at": "2025-10-14T16:00:00",
    "row_count": 0,
    "valid_rows": 0,
    "error_rows": 0
  },
  "message": "File uploaded"
}
```

### GET /api/csv-imports/:id
Get import details with validation preview.

**Response (200):**
```json
{
  "data": {
    "import": {
      "id": 3,
      "status": "pending_validation",
      ...
    },
    "validation": {
      "total_rows": 10,
      "valid_rows": 8,
      "error_rows": 2,
      "rows": [
        {
          "row_number": 2,
          "data": {...},
          "is_valid": true,
          "errors": []
        },
        {
          "row_number": 5,
          "data": {...},
          "is_valid": false,
          "errors": ["Row 5: Insufficient B&W quota"]
        }
      ]
    }
  }
}
```

### POST /api/csv-imports/:id/validate
Validate and import CSV data.

**Request Body (optional corrections):**
```json
{
  "corrections": {
    "5": {
      "bw_quantity": 50
    }
  }
}
```

**Response (200):**
```json
{
  "data": {
    "import_id": 3,
    "imported_orders": [20, 21, 22, 23, 24, 25, 26, 27],
    "import_errors": ["Row 5: Agent workload limit exceeded"],
    "success_count": 8,
    "error_count": 1
  },
  "message": "Import validated and processed"
}
```

### POST /api/csv-imports/:id/reject
Reject CSV import.

**Request Body:**
```json
{
  "notes": "Invalid data format, please correct and resubmit"
}
```

---

## Notifications

### GET /api/notifications
List user notifications.

**Query Parameters:**
- `page` (int): Page number
- `page_size` (int): Items per page
- `unread_only` (boolean): Show only unread

**Response (200):**
```json
{
  "data": {
    "items": [
      {
        "id": 10,
        "message": "✓ Order #15 has been created successfully. B&W: 100, Color: 50",
        "notification_type": "info",
        "is_read": false,
        "created_at": "2025-10-14T10:35:00",
        "related_order_id": 15
      }
    ],
    "pagination": {...},
    "unread_count": 5
  }
}
```

### POST /api/notifications/:id/read
Mark notification as read.

### POST /api/notifications/mark-all-read
Mark all notifications as read.

---

## Reports (Admin Only)

### GET /api/reports/monthly
Export monthly activity report.

**Query Parameters:**
- `month` (string): Month in YYYY-MM format (required)
- `format` (string): Export format (csv, xlsx, pdf)

**Response:**
- CSV: Returns downloadable CSV file
- XLSX: Returns Excel file
- PDF: Returns PDF file

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional context or validation errors"
  }
}
```

### Common Error Codes

- `AUTH_FAILED`: Authentication failed
- `PERMISSION_DENIED`: Insufficient permissions
- `VALIDATION_ERROR`: Input validation failed
- `QUOTA_EXCEEDED`: Order exceeds available quota
- `AGENT_LIMIT_EXCEEDED`: Agent has too many active orders
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource conflict (e.g., duplicate email)
- `DUPLICATE_ROW`: Duplicate external_order_id in CSV
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## Rate Limiting

Authentication endpoints are rate-limited:
- Login: 5 attempts per 5 minutes per IP address

---

## CSV Import Format

### Minimal Format
```csv
client_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes
1,100,50,A4,matte,none,Standard order
```

### Extended Format (with optional fields)
```csv
client_email,agent_email,external_order_id,bw_quantity,color_quantity,paper_dimensions,paper_type,finishing,notes,client_phone
client@example.com,agent@example.com,EXT001,100,50,A4,matte,none,Order note,+1234567890
```

### Required Fields
- One of: `client_id` OR `client_email`
- `bw_quantity` (integer >= 0)
- `color_quantity` (integer >= 0)
- At least one quantity must be > 0

### Optional Fields
- `agent_id` OR `agent_email` (assigns order to agent)
- `external_order_id` (for idempotency)
- `paper_dimensions`, `paper_type`, `finishing`, `notes`
- `client_phone` (validated against E.164 format)

---

## Testing the API

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@versatiles.com","password":"Admin123!"}' \
  -c cookies.txt
```

**Create Order (using saved cookies):**
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"client_id":2,"bw_quantity":100,"color_quantity":50,"paper_dimensions":"A4"}'
```

**Get Quota:**
```bash
curl -X GET "http://localhost:5000/api/quotas?client_id=2" \
  -b cookies.txt
```

---

For more examples, see the sample files in `/samples` directory.
