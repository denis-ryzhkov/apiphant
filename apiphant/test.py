
#### import

from adict import adict, ajson
import json, requests

#### config

config = adict(
    host='127.0.0.1',
    port=8888,
    version='v0',
) # Can be updated from a caller script.

#### test

def test(target, action, request_json, status_code, response_json, method='POST'):

    url = 'http://{host}:{port}/api/{version}/{target}/{action}'.format(target=target, action=action, **config)
    request_json = json.dumps(request_json) if request_json else None

    print('{method} {url} {request_json} --> {status_code} {response_json}'.format(**locals()))
    response = requests.request(method, url, data=request_json)

    assert response.status_code == status_code, (response.status_code, status_code, response.text)
    response.ajson = ajson(response.json())
    assert response.ajson == response_json, (response.text, response_json)
    # NOTE: response.text is used instead of response.ajson|json() to easily compare without extra u'...'-s.

    return response
