#!./test.sh

#### import

from apiphant.test import test

#### test echo

test('echo', 'read', {"hello": "world"}, 200, {"hello": "world", "server": "myproduct"})

#### test apiphant internals

#### apiphant.server.serve.app

test('self', 'delete', None, 404, {"error": "404 Not Found"})
test('self', 'create', None, 501, {"error": "501 Not Implemented"}, method='GET')

test('self', 'create', 'invalid_json_object', 400, {"error": "Request content should be JSON Object"})
test('self', 'create', {"test": "return invalid_json_object"}, 500, {"error": "500 Internal Server Error"})

test('self', 'create', {"test": "1/0"}, 500, {"error": "500 Internal Server Error"})
test('self', 'create', None, 200, {"ok": True, "x": None})

#### apiphant.validation.field

test('self', 'create', {"test": "optional"}, 200, {"ok": True, "x": None})
test('self', 'create', {"test": "default"}, 200, {"ok": True, "x": "X"})

test('self', 'create', {"test": "required"}, 400, {"error": "x is Missing"})
test('self', 'create', {"test": "required", "x": "X"}, 200, {"ok": True, "x": "X"})

test('self', 'create', {"test": "valid_value", "x": "Y"}, 400, {"error": "x is Invalid"})
test('self', 'create', {"test": "valid_value", "x": "X"}, 200, {"ok": True, "x": "X"})

test('self', 'create', {"test": "valid_type", "x": "X"}, 400, {"error": "x is Invalid"})
test('self', 'create', {"test": "valid_type", "x": 42}, 200, {"ok": True, "x": 42})

test('self', 'create', {"test": "valid_length", "x": ["X"]}, 400, {"error": "x is Invalid"})
test('self', 'create', {"test": "valid_length", "x": ["X", "Y"]}, 200, {"ok": True, "x": ["X", "Y"]})

test('self', 'create', {"test": "max_length", "x": "123"}, 400, {"error": "x is Invalid"})
test('self', 'create', {"test": "max_length", "x": "12"}, 200, {"ok": True, "x": "12"})
test('self', 'create', {"test": "max_length", "x": "1"}, 200, {"ok": True, "x": "1"})

#### total

print('OK')
