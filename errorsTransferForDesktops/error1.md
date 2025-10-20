(venv) PS C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint> python run.py
Starting VersatilesPrint application in development mode...
Server running on http://0.0.0.0:5000
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
Press CTRL+C to quit
 * Restarting with stat
Starting VersatilesPrint application in development mode...
Server running on http://0.0.0.0:5000
 * Debugger is active!
 * Debugger PIN: 753-860-107
127.0.0.1 - - [20/Oct/2025 12:21:53] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Oct/2025 12:21:53] "GET /static/css/style.css HTTP/1.1" 200 -
127.0.0.1 - - [20/Oct/2025 12:21:53] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [20/Oct/2025 12:22:03] "GET /login HTTP/1.1" 200 -
127.0.0.1 - - [20/Oct/2025 12:22:03] "GET /static/css/style.css HTTP/1.1" 304 -
127.0.0.1 - - [20/Oct/2025 12:22:26] "POST /api/auth/login HTTP/1.1" 500 -
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
pymysql.err.ProgrammingError: (1146, "Table 'versatiles_print.users' doesn't exist")

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
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\utils\decorators.py", line 194, in decorated_function    
    return f(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\api\auth.py", line 37, in login
    success, user, error = AuthService.authenticate(
                           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\services\auth_service.py", line 30, in authenticate      
    user = User.get_by_email(email)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\models\user.py", line 139, in get_by_email
    return session.query(cls).filter(cls.email == email).first()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\sqlalchemy\orm\query.py", line 2728, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in rai    packet.raise_for_error()
    packet.raise_for_error()
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
    err.raise_mysql_exception(self._data)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
    raise errorclass(errno, errval)
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.users' doesn't exist")
[SQL: SELECT users.id AS users_id, users.email AS users_email, users.password_hash AS users_password_hash, users.full_name AS users_full_name, users.role_id AS users_role_id, users.created_at AS users_created_at, users.is_active AS users_is_active, users.last_login AS users_last_login 
FROM users
WHERE users.email = %(email_1)s
 LIMIT %(param_1)s]
[parameters: {'email_1': 'admin@versatiles.com', 'param_1': 1}]
(Background on this error at: https://sqlalche.me/e/20/f405)




