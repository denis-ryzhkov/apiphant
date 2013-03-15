Apiphant
========

Simple Python Web API framework, based on Gevent, JSON, CRUD.

Features:

* Based on [gevent.wsgi][], optimized for tens of thousands of concurrent users.
[gevent.wsgi]: http://www.gevent.org/servers.html

* Simple!  
Try it:
```
    mkdir -p myproduct/api/v0
    touch {myproduct,myproduct/api,myproduct/api/v0}/__init__.py

    cat <<END >myproduct/api/v0/echo.py
    # from myproduct.api import anything
    def read(request):
        response = request.copy()
        response.ok = True
        return response
    END

    sudo apt-get install --yes gcc libevent-dev python-dev
    sudo pip install apiphant
    apiphant myproduct localhost:8100

    # POST http://{host}:{port}/api/{version}/{t/a/r/g/e/t}/{action}
    curl --data-binary '{"hello": "world"}' --request POST http://localhost:8100/api/v0/echo/read
    {"hello": "world", "ok": true}
```

* `version` value `v0` used in the example
[means](http://semver.org/) API is not public yet, and maybe never will,
so is expected to be changed without notification.

* `action` is one of [CRUD][]: `create`, `read`, `update`, `delete`.
* Reasons why [CRUD][] is implemented without use of HTTP methods
that are recommended by [REST][]:
    * Best match for generally partial «Update» action is [PATCH][] method,
    but it is not supported by our [gevent.wsgi][] webserver and several clients.
    * Much more standard `PUT` method means «Replace»,
    that is not how «Update» should work in general case.
    Imagine SQL `UPDATE` working as «Replace».
    * Some cases allow only `GET` and `POST`,
    e.g. cross-origin requests in some browsers,
    while at least `DELETE` method is required for full set of actions.
    * So `POST` is selected as «a uniform method», suitable for all actions:
    «The actual function performed by the POST method
    is determined by the server» - [HTTP/1.1][].
[CRUD]: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[REST]: http://en.wikipedia.org/wiki/Representational_state_transfer
[PATCH]: http://tools.ietf.org/html/rfc5789
[HTTP/1.1]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html

* [`{"json": "object"}`][JSON] is used for both request and response,
to speak one language easily with any client.
    * No [`X-Custom-HTTP: Headers`][custom HTTP headers].
    * No [`?a=url%20encoded%20query%20string`][urlencoded querystring].
    * No need to check the type of root [JSON][] value,
    it is always object with self-describing names inside,
    not just bare value like `42`.
[JSON]: http://json.org/
[custom HTTP headers]: http://www.google.com/search?q=custom+http+headers
[urlencoded querystring]: http://en.wikipedia.org/wiki/Query_string#URL_encoding

* However, URL still contains several request parameters, because:
    * Different targets may be routed by load balancers
    to different backend servers using simple URL location routing.
    * `version`, `target` and `action` are always required,
    so may be positional parameters,
    improving readability and saving resources in a natural way.

* TODO: tests.

* TODO: `nginx` and `supervisor` config examples.

apiphant version 0.1.0  
Copyright (C) 2013 by Denis Ryzhkov <denisr@denisr.com>  
MIT License, see http://opensource.org/licenses/MIT
