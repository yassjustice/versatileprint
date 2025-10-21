Quota API response: {data: {…}}data: bw: {available: 3000, base_limit: 3000, percentage_used: 0, topups: 0, total_limit: 3000, …}client_id: 2color: {available: 2000, base_limit: 2000, percentage_used: 0, topups: 0, total_limit: 2000, …}month: "2025-10-01"topups_history: [][[Prototype]]: Object[[Prototype]]: Object
dashboard:417 Orders API response: {data: {…}}data: items: []pagination: {has_next: false, has_prev: false, page: 1, page_size: 20, total_items: 0, …}[[Prototype]]: Object[[Prototype]]: Object
dashboard:481  POST http://127.0.0.1:5000/api/orders 400 (BAD REQUEST)
(anonymous) @ dashboard:481

## ERROR DESCRIPTION
- on the client view, the quota data isn't diplaying at all; all I got is :  My Quota
No quota information available.
- creating an order isn't working anf the ui for it has no clear error message; 