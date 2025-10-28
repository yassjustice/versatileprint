## Raw Errors
dashboard:1234  PATCH http://127.0.0.1:5000/api/orders/2/assign 500 (INTERNAL SERVER ERROR)
confirmBtn.onclick @ dashboard:1234
dashboard:1251 Error assigning order: SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON
## ERROR DESCRIPTION
- assigning the order to the agent by the admin works in backend and fails in the frontend;
- channging status doesn't work at all 
- changing the name for the agent by the admin shows no errors but doens't change the name at all - it's just non responding
- dashboard metrics for agent view is not displaying any data, all is 0
- The agent account view has No updated order management using reusable components 
- the agent cannot currently change the status of the orders asssigned to him