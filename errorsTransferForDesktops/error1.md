## Raw Errors
dashboard:495 
 POST http://127.0.0.1:5000/api/orders 400 (BAD REQUEST)
(anonymous)	@	dashboard:495
dashboard:502 Create order response: 
{error: {…}}
dashboard:413  GET http://127.0.0.1:5000/api/orders 500 (INTERNAL SERVER ERROR)
(anonymous) @ dashboard:413
dashboard:463 Error loading orders: SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON
127.0.0.1 - - [21/Oct/2025 14:26:03] "GET /api/orders HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1625, in _object_value_for_elem
    return self._object_lookup[elem]
           ^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'pending'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 1478, in __call__ 
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 1458, in wsgi_app 
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 1455, in wsgi_app 
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 869, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 867, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 852, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\api\orders.py", line 23, in list_orders
    result = OrderService.get_orders_for_user(current_user, status, page, page_size)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\services\order_service.py", line 218, in get_orders_for_user
    orders = Order.get_by_client(user.id, status)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\models\order.py", line 146, in get_by_client
    return query.all()
           ^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2673, in all
    return self._iter().all()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1769, in all
    return self._allrows()
           ^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 548, in _allrows
    rows = self._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 1676, in _fetchall_impl
    return self._real_result._fetchall_impl()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 2270, in _fetchall_impl
    return list(self.iterator)
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\loading.py", line 219, in chunks
    fetch = cursor._raw_all_rows()
            ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 541, in _raw_all_rows
    return [make_row(row) for row in rows]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\result.py", line 541, in <listcomp>
    return [make_row(row) for row in rows]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "lib\\sqlalchemy\\cyextension\\resultproxy.pyx", line 22, in sqlalchemy.cyextension.resultproxy.BaseRow.__init__
  File "lib\\sqlalchemy\\cyextension\\resultproxy.pyx", line 79, in sqlalchemy.cyextension.resultproxy._apply_processors
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1745, in process
    value = self._object_value_for_elem(value)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\dialects\mysql\enumerated.py", line 87, in _object_value_for_elem
    return super()._object_value_for_elem(elem)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\sqltypes.py", line 1627, in _object_value_for_elem
    raise LookupError(
LookupError: 'pending' is not among the defined enum values. Enum name: orderstatus. Possible values: PENDING, VALIDATED, PROCESSING, COMPLETED


## ERROR DESCRIPTION
- creating an order isn't working yet but it seems like the quota got used by a failed request of creating an order :
- On the UI: 
    My Quota
    B&W: 24 / 3000 prints (0.8% used)

    0.8%
    Color: 24 / 2000 prints (1.2% used)

    1.2%
- Quota management is working fine for no but it's counting even the erroneous orders! either they get created but display an error or they get the quota management is counting the failed orders! which is dangerous and should be checked deeply
- Orders aren't showing on the table on the Ui for it and it shows : 
        My Orders
    Failed to load orders


