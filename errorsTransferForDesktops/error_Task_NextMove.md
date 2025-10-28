## Raw Errors
dashboard:686 Uncaught SyntaxError: Identifier 'viewOrderDetails' has already been declared (at dashboard:686:9)
    at dashboard:686:9
(anonymous) @ dashboard:686
favicon.ico:1  GET http://127.0.0.1:5000/favicon.ico 500 (INTERNAL SERVER ERROR)
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /login HTTP/1.1" 302 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /dashboard HTTP/1.1" 200 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /static/js/app.js HTTP/1.1" 304 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /static/css/style.css HTTP/1.1" 304 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /static/js/components.js HTTP/1.1" 304 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /api/notifications?limit=5 HTTP/1.1" 200 -
127.0.0.1 - - [28/Oct/2025 12:15:14] "GET /favicon.ico HTTP/1.1" 500 -
Traceback (most recent call last):
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 867, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 841, in dispatch_request
    self.raise_routing_exception(req)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 450, in raise_routing_exception
    raise request.routing_exception  # type: ignore
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\ctx.py", line 353, in match_request
    result = self.url_adapter.match(return_rule=True)  # type: ignore
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\werkzeug\routing\map.py", line 624, in match
    raise NotFound() from None
werkzeug.exceptions.NotFound: 404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

During handling of the above exception, another exception occurred:

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
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 752, in handle_user_exception
    return self.handle_http_exception(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\app.py", line 727, in handle_http_exception
    return self.ensure_sync(handler)(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\__init__.py", line 149, in not_found
    return render_template('errors/404.html'), 404
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\flask\templating.py", line 151, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\loaders.py", line 138, in load 
    code = environment.compile(source, name, filename)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\environment.py", line 771, in compile
    self.handle_exception(source=source_hint)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\venv\Lib\site-packages\jinja2\environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "C:\Users\USER2\Desktop\RECORDS\DevCreation\PrintingCompany\versatileprint\app\templates\errors\404.html", line 5, in template
    {% block title %}404 - Page Not Found{% endblock %}
jinja2.exceptions.TemplateAssertionError: block 'title' defined twice
127.0.0.1 - - [28/Oct/2025 12:15:44] "GET /api/notifications?limit=5 HTTP/1.1" 200 -

## ERROR DESCRIPTION
