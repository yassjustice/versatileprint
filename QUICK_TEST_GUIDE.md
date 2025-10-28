# Quick Testing Guide

## Prerequisites
1. Restart the Flask application to apply all changes
2. Have test accounts ready for each role: Admin, Agent, Client

---

## Test Sequence

### Part 1: Admin - Order Assignment (Fix #1)

1. **Login as Admin**
2. **Navigate to Dashboard → All Orders tab**
3. **Test Assignment:**
   - Click the person icon (👤+) on any order
   - Select an agent from dropdown
   - Click "Assign"
   - ✅ **Expected:** Success toast, no 500 error, order shows assigned agent

4. **Test Unassignment:**
   - Click person icon on assigned order
   - Select "Unassigned" from dropdown
   - Click "Assign"
   - ✅ **Expected:** Success toast, agent removed

5. **Test Error Handling:**
   - Try assigning to agent at capacity (if applicable)
   - ✅ **Expected:** Proper error message (not HTML page)

---

### Part 2: Admin - Status Changes (Fix #2)

1. **Still as Admin**
2. **Test Status Progression:**
   - Click "View/Edit" (eye icon) on a pending order
   - Change status dropdown to "Validated"
   - Click "Change Status"
   - ✅ **Expected:** Success toast, status updates

3. **Continue the workflow:**
   - Validated → Processing
   - Processing → Completed
   - ✅ **Expected:** Each transition works, proper validation

---

### Part 3: Admin - User Updates (Fix #3)

1. **Still as Admin**
2. **Navigate to Dashboard → Users tab**
3. **Test Name Update:**
   - Click "Edit" (pencil icon) on any user
   - Change "Full Name" field
   - Click "Save Changes"
   - ✅ **Expected:** Success toast
   - Refresh page
   - ✅ **Expected:** Name change persists

4. **Check Browser Console Logs:**
   - Should see log: "Updating user X with data: ..."
   - Should see log: "Updated full_name to: ..."
   - Should see log: "User X updated successfully"

---

### Part 4: Agent - Dashboard Metrics (Fix #4)

1. **Logout and Login as Agent**
2. **View Dashboard:**
   - ✅ **Expected:** Active Orders count > 0 (if agent has orders)
   - ✅ **Expected:** Completed Orders count shows correct number
   - ✅ **Expected:** Workload Capacity shows "X/10" (not "0/10")

3. **Verify Cards:**
   - If active orders >= 8: Border should be warning (yellow/orange)
   - If active orders >= 10: Border should be danger (red)

---

### Part 5: Agent - Order Management UI (Fix #5)

1. **Still as Agent**
2. **Verify Order Table:**
   - ✅ **Expected:** Professional table with DataTable component
   - ✅ **Expected:** Status badges are color-coded
   - ✅ **Expected:** Action buttons (eye, arrow) visible

3. **Test View Details:**
   - Click "View Details" (eye icon) on any order
   - ✅ **Expected:** Modal opens with order information
   - ✅ **Expected:** All fields populated correctly
   - ✅ **Expected:** "Advance Status" button visible (unless completed)

4. **Test Table Features:**
   - Click on column headers to sort
   - ✅ **Expected:** Sorting works
   - If >20 orders: Check pagination
   - ✅ **Expected:** Pagination works

---

### Part 6: Agent - Status Changes (Fix #6)

1. **Still as Agent**
2. **From Order Table:**
   - Click "Advance Status" (arrow icon) on pending order
   - ✅ **Expected:** Confirmation dialog appears
   - Click OK
   - ✅ **Expected:** Loading spinner → Success toast → Page reloads
   - ✅ **Expected:** Order status now "Validated"

3. **From Order Details Modal:**
   - Click "View Details" on validated order
   - Click "Advance Status" button in modal
   - ✅ **Expected:** Confirmation dialog
   - Click OK
   - ✅ **Expected:** Status advances to "Processing"

4. **Continue Workflow:**
   - Advance Processing → Completed
   - Open completed order details
   - ✅ **Expected:** "Advance Status" button is hidden

5. **Test Button Labels:**
   - Pending order: Button says "Validate"
   - Validated order: Button says "Start Processing"
   - Processing order: Button says "Complete"

---

## Error Cases to Test

### Invalid Operations

1. **As Agent, try to change another agent's order:**
   - Open browser DevTools → Console
   - Run: `fetch('/api/orders/[other_agent_order_id]/status', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status:'validated'})}).then(r=>r.json()).then(console.log)`
   - ✅ **Expected:** Error response "You can only change status of orders assigned to you"

2. **As Client, try to change order status:**
   - Login as Client
   - Try to use API directly (console)
   - ✅ **Expected:** "Clients cannot change order status"

3. **Invalid Status Transition:**
   - Try to skip a status (e.g., Pending → Completed)
   - ✅ **Expected:** Validation error about allowed transitions

---

## Browser Console Checks

Throughout testing, monitor browser console for:
- ❌ No JavaScript errors
- ❌ No "Unexpected token" JSON parse errors
- ❌ No 500 Internal Server Errors
- ✅ API responses are valid JSON
- ✅ Success messages logged for actions

---

## Network Tab Checks

In Browser DevTools → Network:
1. Filter by "Fetch/XHR"
2. For each action, check:
   - ✅ Status Code: 200, 201, 400, 403, 404 (NO 500s)
   - ✅ Response Type: JSON (not HTML)
   - ✅ Response has proper structure: `{data: {...}, message: "..."}`

---

## Logs to Check

### Server Logs
In `logs/` directory or console output:
- ✅ "Updating user X with data: ..." (for user updates)
- ✅ "User X updated successfully"
- ✅ "ORDER_STATUS_CHANGE" audit log entries
- ✅ "ORDER_ASSIGNED" / "ORDER_REASSIGNED" audit log entries
- ❌ No unhandled exceptions or stack traces

---

## Success Indicators

### Visual Checks
- ✅ All modals open/close smoothly
- ✅ Toast notifications appear and auto-dismiss
- ✅ Loading spinners show during API calls
- ✅ Tables render with proper formatting
- ✅ Badges have correct colors
- ✅ Buttons are properly labeled

### Functional Checks
- ✅ All CRUD operations work
- ✅ Data persists after refresh
- ✅ Role-based access is enforced
- ✅ Status workflows are validated
- ✅ Agent metrics are accurate

### Technical Checks
- ✅ All API responses are JSON
- ✅ No 500 errors in any scenario
- ✅ Error messages are user-friendly
- ✅ Console is clean (no errors)
- ✅ Network requests return proper status codes

---

## If Issues Arise

1. **Check Browser Console:**
   - Look for JavaScript errors
   - Check network tab for failed requests

2. **Check Server Logs:**
   - Look for Python exceptions
   - Check for database errors

3. **Verify Changes Were Applied:**
   - Restart Flask app
   - Clear browser cache
   - Hard refresh (Ctrl+F5)

4. **Report Issue:**
   - Note which fix number
   - Copy error message
   - Include browser console logs
   - Include server logs if available

---

## Time Estimate

- **Quick Test (Essential):** 10-15 minutes
- **Comprehensive Test (All scenarios):** 30-45 minutes
- **Full Regression Test:** 1-2 hours

---

## Priority Order

If time is limited, test in this order:
1. **Fix #4** (Agent metrics) - Most critical, easiest to verify
2. **Fix #1** (Order assignment) - Was causing 500 errors
3. **Fix #6** (Agent status changes) - Core functionality
4. **Fix #2** (Status change endpoint) - Related to #6
5. **Fix #5** (Agent UI) - UI enhancement
6. **Fix #3** (User updates) - Lower priority

---

## Done!

When all tests pass:
- ✅ Mark fixes as verified
- ✅ Update project status
- ✅ Inform stakeholders
- ✅ Deploy to production (if applicable)
