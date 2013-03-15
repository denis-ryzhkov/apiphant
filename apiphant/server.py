
#### serve

def serve(product_path, host, port):

    #### become cooperative

    import gevent.monkey
    gevent.monkey.patch_all()

    #### import

    from adict import adict
    from apiphant.validation import ApiError, status_by_code
    import gevent.wsgi
    import json, os, re, sys
    from traceback import print_exc

    #### paths

    product_path = os.path.abspath(product_path) # /absolutized/path/to/myproduct

    api_path = os.path.join(product_path, 'api') # /absolutized/path/to/myproduct/api
    if not os.path.isdir(api_path):
        exit('Dir not found: {api_path}'.format(api_path=api_path))

    product_parent_path, product_name = os.path.split(product_path.rstrip(os.sep)) # /absolutized/path/to, myproduct
    sys.path.insert(0, product_parent_path) # Now it is possible: from myproduct.api import anything

    #### routes

    def routes():

        '''Creates map of routes from PATH_INFO to action().'''

        routes = dict()
        version_re = re.compile('^v\d+$')
        py_extension = '.py'

        for version in os.listdir(api_path):
            if not os.path.isdir(version) or not version_re.match(version):
                continue

            for target_file_name in os.listdir(os.path.join(api_path, version)):
                if not target_file_name.endswith(py_extension):
                    continue

                target_name = target_file_name[:-len(py_extension)]
                # TODO: Add support for nested t/a/r/g/e/t-s.
                target_module = __import__('{product_name}.api.{version}.{target_name}'.format(**locals()), globals(), locals())

                for action_name in 'create', 'read', 'update', 'delete':
                    action = getattr(getattr(getattr(target_module.api, version), target_name), action_name, None)
                    if not action:
                        continue

                    routes['/api/{version}/{target_name}/{action_name}'.format(**locals())] = action

        return routes

    routes = routes()

    #### finish_response

    def finish_response(start_response, status, response):

        start_response(status=status, headers=(
            ('Content-Type', 'application/json'),
        ))

        return [
            json.dumps(response),
        ]

    #### app

    def app(environ, start_response):

        try:

            if environ['REQUEST_METHOD'] != 'POST': # See README.md.
                raise ApiError(501)

            action = routes.get(environ['PATH_INFO'])
            if not action:
                raise ApiError(404)

            request = environ['wsgi.input'].read()
            try:
                request = json.loads(request) if request else {}
                if not isinstance(request, dict):
                    raise ValueError
            except ValueError:
                raise ApiError(400, 'Request content should be JSON Object') # See README.md.
            request = adict(request)

            response = action(request)

            if response is None:
                response = {}

            if not isinstance(response, dict):
                raise Exception('Response content should be JSON Object') # See README.md.

            return finish_response(start_response, status_by_code[200], response)

        except ApiError as e: # Expected error, no logging.
            status = status_by_code[e.status_code]
            return finish_response(start_response, status, dict(error=(e.error or status)))

        except: # Unexpected error, traceback is logged.
            print_exc()
            status = status_by_code[500]
            return finish_response(start_response, status, dict(error=status)) # Server error details are saved to log and not disclosed to a client.

    #### gevent.serve

    print('Apiphant is serving {api_path} at http://{host}:{port}/api'.format(**locals()))
    gevent.wsgi.WSGIServer((host, port), app).serve_forever()

#### main

def main():

    #### import

    import os, sys

    #### command-line config

    usage = 'Usage: apiphant path/to/myproduct host:port'

    try:
        _, product_path, host_port = sys.argv
        last_colon_index = host_port.rindex(':') # Not split(), because IPv6 host may contain colons.
    except ValueError:
        exit(usage)

    host, port = host_port[:last_colon_index], host_port[last_colon_index + 1:]

    #### serve

    serve(product_path, host, port)
