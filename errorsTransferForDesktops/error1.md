dashboard:399  GET http://127.0.0.1:5000/api/orders 500 (INTERNAL SERVER ERROR)
(anonymous) @ dashboard:399
VM266:1 Uncaught (in promise) SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON
dashboard:493  GET http://127.0.0.1:5000/api/notifications?limit=5 500 (INTERNAL SERVER ERROR)
loadNotifications @ dashboard:493
(anonymous) @ dashboard:516
dashboard:512 Failed to load notifications: SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON

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
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\api\notifications.py", line 21, in list_notifications    
    notifications = Notification.get_for_user(current_user.id, unread_only)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\models\notification.py", line 81, in get_for_user        
    return query.all()
           ^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2673, in all
    return self._iter().all()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2827, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2362, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2247, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 305, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1418, in execute
    return meth(
           ^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 515, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1640, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2355, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
    conn.query(q)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
    result.read()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.notifications' doesn't exist")
[SQL: SELECT notifications.id AS notifications_id, notifications.user_id AS notifications_user_id, notifications.message AS notifications_message, notifications.related_order_id AS notifications_related_order_id, notifications.is_read AS notifications_is_read, notifications.created_at AS notifications_created_at, notifications.notification_type AS notifications_notification_type
FROM notifications
WHERE notifications.user_id = %(user_id_1)s ORDER BY notifications.created_at DESC]
[parameters: {'user_id_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/f405)
127.0.0.1 - - [20/Oct/2025 13:43:14] "GET /api/notifications?limit=5 HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
    conn.query(q)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
    result.read()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'versatiles_print.notifications' doesn't exist")

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
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\api\notifications.py", line 21, in list_notifications    
    notifications = Notification.get_for_user(current_user.id, unread_only)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\models\notification.py", line 81, in get_for_user        
    return query.all()
           ^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2673, in all
    return self._iter().all()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2827, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2362, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2247, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 305, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1418, in execute
    return meth(
           ^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 515, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1640, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2355, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
    conn.query(q)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
    result.read()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.notifications' doesn't exist")
[SQL: SELECT notifications.id AS notifications_id, notifications.user_id AS notifications_user_id, notifications.message AS notifications_message, notifications.related_order_id AS notifications_related_order_id, notifications.is_read AS notifications_is_read, notifications.created_at AS notifications_created_at, notifications.notification_type AS notifications_notification_type
FROM notifications
WHERE notifications.user_id = %(user_id_1)s ORDER BY notifications.created_at DESC]
[parameters: {'user_id_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/f405)
127.0.0.1 - - [20/Oct/2025 13:43:44] "GET /api/notifications?limit=5 HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
    conn.query(q)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
    result.read()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
pymysql.err.ProgrammingError: (1146, "Table 'versatiles_print.notifications' doesn't exist")

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
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\api\notifications.py", line 21, in list_notifications    
    notifications = Notification.get_for_user(current_user.id, unread_only)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\models\notification.py", line 81, in get_for_user        
    return query.all()
           ^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2673, in all
    return self._iter().all()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2827, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2362, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\session.py", line 2247, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\context.py", line 305, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1418, in execute
    return meth(
           ^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\sql\elements.py", line 515, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1640, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 2355, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\engine\default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 153, in execute
    result = self._query(query)
             ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\cursors.py", line 322, in _query
    conn.query(q)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 558, in query
    self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
    result.read()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 1200, in read
    first_packet = self.connection._read_packet()
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.notifications' doesn't exist")
[SQL: SELECT notifications.id AS notifications_id, notifications.user_id AS notifications_user_id, notifications.message AS notifications_message, notifications.related_order_id AS notifications_related_order_id, notifications.is_read AS notifications_is_read, notifications.created_at AS notifications_created_at, notifications.notification_type AS notifications_notification_type
FROM notifications
WHERE notifications.user_id = %(user_id_1)s ORDER BY notifications.created_at DESC]
[parameters: {'user_id_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/f405)
