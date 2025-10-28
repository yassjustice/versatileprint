# Admin Order Management Guide

## Overview
This guide explains how to use the new order management features in the Admin dashboard.

---

## Features

### 1. **View Order Details**
Click the **eye icon** (👁️) in the orders table to view complete order information.

**What you can see**:
- Order ID and current status
- Client information
- Assigned agent (if any)
- Print quantities (B&W and Color)
- Paper specifications (size, type, finishing)
- Order notes
- Creation and update timestamps

---

### 2. **Change Order Status**

**Steps**:
1. Open order details (click eye icon)
2. Select new status from the "Status" dropdown:
   - **Pending** → Initial state
   - **Validated** → Admin approved
   - **Processing** → Being worked on
   - **Completed** → Finished
3. Click **"Change Status"** button
4. Confirmation toast will appear
5. Page reloads with updated status

**Allowed Transitions**:
- Pending → Validated
- Validated → Processing
- Processing → Completed

---

### 3. **Assign Order to Agent**

#### **Method 1: Quick Assign (Recommended)**
1. Click the **person-plus icon** (👤+) in the orders table
2. A dialog appears with agent dropdown
3. Select an agent from the list
   - Shows agent name and current workload (e.g., "John Doe (5/10)")
   - "(5/10)" means agent has 5 active orders out of max 10
4. Click **"Assign"** to confirm
5. Success notification appears
6. Page reloads

#### **Method 2: Full Modal Assign**
1. Click the **eye icon** to open order details
2. In the "Assigned Agent" dropdown, select an agent
3. Click **"Assign Agent"** button at bottom
4. Success notification appears
5. Page reloads

**Unassigning an Order**:
- In either method, select **"Unassigned"** from the dropdown
- Order will be removed from agent's workload

---

### 4. **Agent Capacity Management**

**Understanding Capacity**:
- Each agent has a maximum of **10 active orders** (default)
- Active orders = orders in Pending, Validated, or Processing status
- Completed orders don't count toward capacity

**What happens when capacity is reached**:
- Assignment will fail with error message
- You'll see: "Agent workload limit exceeded. Active orders: 10/10"
- Must wait for agent to complete orders OR reassign some orders

**Viewing Agent Workload**:
- In assignment dialog: Shows as "(current/max)" next to agent name
- Example: "Jane Smith (8/10)" means Jane has 8 active orders

---

## Tips & Best Practices

### ✅ DO:
- Check agent workload before assigning
- Distribute orders evenly among agents
- Update status as orders progress
- Use the quick assign for faster workflows
- Unassign orders if agent is overloaded

### ❌ DON'T:
- Assign to agents at full capacity
- Skip status transitions (e.g., Pending → Completed)
- Leave orders unassigned for too long
- Reassign without checking current agent workload

---

## Keyboard Shortcuts
- `ESC` - Close any open modal
- `Enter` (in dropdowns) - Confirm selection

---

## Troubleshooting

### "Failed to load order details"
- **Cause**: Network issue or order not found
- **Solution**: Refresh page and try again

### "Agent workload limit exceeded"
- **Cause**: Agent has 10 active orders
- **Solution**: 
  1. Choose a different agent
  2. Wait for agent to complete orders
  3. Reassign some of agent's orders to others

### "Failed to assign order"
- **Cause**: Permission issue or agent inactive
- **Solution**: Verify agent account is active

### Modal doesn't open / JavaScript errors
- **Cause**: Browser cache or script loading issue
- **Solution**: 
  1. Hard refresh page (Ctrl+Shift+R or Cmd+Shift+R)
  2. Clear browser cache
  3. Check browser console for errors

---

## API Endpoints Used

For developers/advanced users:

- `GET /api/orders/{id}` - Fetch order details
- `POST /api/orders/{id}/status` - Change order status
- `PATCH /api/orders/{id}/assign` - Assign/unassign agent
- `GET /api/users?role=Agent` - Get list of agents with capacity

---

## Notifications

**Who gets notified**:
- **Agent**: When order is assigned to them
- **Previous Agent**: When order is reassigned away
- **Client**: When order status changes

**Notification Methods**:
- In-app notification badge (🔔)
- Email (if configured)

---

## Audit Trail

All order management actions are logged:
- Status changes (who changed, when, from → to)
- Agent assignments (who assigned, which agent)
- Unassignments

Access audit logs via Reports section.

---

## Support

For issues or questions:
1. Check this guide first
2. Review error messages in browser console (F12)
3. Contact system administrator
4. Report bugs via your issue tracking system

---

**Last Updated**: October 28, 2025
**Version**: 1.0
