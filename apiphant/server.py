
#### raw_environ

def raw_environ(action):
    action.raw_environ = True
    return action

#### serve

def serve(product_path, host, port):

    #### become cooperative

    import gevent.monkey
    gevent.monkey.patch_all()

    #### import

    from adict import adict
    from apiphant.paths import init_paths
    from apiphant.validation import ApiError, status_by_code
    import gevent.wsgi
    import json, logging, os, re, sys
    from traceback import print_exc

    #### paths

    api_path, product_name = init_paths(product_path)

    #### routes

    def routes():

        '''Creates map of routes from PATH_INFO to action().'''

        routes = dict()
        version_re = re.compile('^v\d+$')
        py_extension = '.py'

        for version in os.listdir(api_path):
            version_path = os.path.join(api_path, version)
            if not os.path.isdir(version_path) or not version_re.match(version):
                continue

            for target_file_name in os.listdir(version_path):
                if not target_file_name.endswith(py_extension):
                    continue

                target_name = target_file_name[:-len(py_extension)]
                # TODO: Add support for nested t/a/r/g/e/t-s.
                target_module = __import__(
                    '{product_name}.api.{version}.{target_name}'.format(
                        product_name=product_name,
                        version=version,
                        target_name=target_name,
                    ),
                    globals(), locals(),
                )

                for action_name in 'create', 'read', 'update', 'delete':
                    action = getattr(getattr(getattr(target_module.api, version), target_name), action_name, None)
                    if not action:
                        continue

                    routes['/api/{version}/{target_name}/{action_name}'.format(**locals())] = action

        return routes

    routes = routes()

    #### finish_response

    def finish_response(start_response, status, response):

        start_response(status=status, headers=[
            ('Content-Type', 'application/json'),
        ])

        return [
            response,
        ]

    #### app

    def app(environ, start_response):

        try:

            action = routes.get(environ['PATH_INFO'])
            if not action:
                raise ApiError(404)

            #### raw_environ

            if hasattr(action, 'raw_environ'):
                response = action(environ)

            #### normal request

            else:

                if environ['REQUEST_METHOD'] != 'POST': # See README.md.
                    raise ApiError(501)

                request = environ['wsgi.input'].read()

                try:
                    request = json.loads(request) if request else {}
                    if not isinstance(request, dict):
                        raise ValueError

                except ValueError:
                    raise ApiError(400, 'Request content should be JSON Object') # See README.md.

                request = adict(request)

                response = action(request)

            #### normal response

            if response is None:
                response = {}

            if not isinstance(response, dict):
                raise Exception('Response content should be JSON Object') # See README.md.

            return finish_response(start_response, status_by_code[200], json.dumps(response))

        #### Expected error, no logging.

        except ApiError as e:
            status = status_by_code[e.status_code]
            return finish_response(start_response, status, json.dumps(dict(error=(e.error or status))))

        #### Unexpected error, traceback is logged.

        except:
            print_exc() # To sys.stderr.
            status = status_by_code[500]
            return finish_response(start_response, status, json.dumps(dict(error=status))) # Server error details are saved to log and not disclosed to a client.

    #### logging

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s at %(module)s.%(funcName)s:%(lineno)d [%(asctime)s] %(message)s') # To sys.stderr by default.
    logging.info('\nApiphant is serving {api_path} at http://{host}:{port}/api\n'.format(**locals()))

    #### gevent.serve

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
        host, port = host_port[:last_colon_index], int(host_port[last_colon_index + 1:])
    except ValueError:
        exit(usage)

    #### serve

    serve(product_path, host, port)
