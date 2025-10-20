Connecting to database...
Database URL: localhost:3306/versatiles_print

✓ Database connection successful

Reading schema from schema.sql...

Executing 2 SQL statements...

  Warning on statement 1: (pymysql.err.ProgrammingError) (1064, 'You have an error in your SQL syntax; check the manual that c

  Warning on statement 2: (pymysql.err.ProgrammingError) (1064, "You have an error in your SQL syntax; check the manual that c
✓ Schema created successfully

Seeding initial data...

✗ Error: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.roles' doesn't exist")
[SQL: SELECT id, name FROM roles]
(Background on this error at: https://sqlalche.me/e/20/f405)
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
pymysql.err.ProgrammingError: (1146, "Table 'versatiles_print.roles' doesn't exist")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\scripts\init_db.py", line 78, in init_database
    result = conn.execute(text("SELECT id, name FROM roles"))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) (1146, "Table 'versatiles_print.roles' doesn't exist")
[SQL: SELECT id, name FROM roles]
(Background on this error at: https://sqlalche.me/e/20/f405)
(venv) PS C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint> 