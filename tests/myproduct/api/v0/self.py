#### import

from apiphant.validation import field, Invalid

#### create

def create(request):

    '''Self-tests of apiphant internals.'''

    test = field(request, 'test', is_required=False)

    #### apiphant.server.serve.app

    if test == 'return invalid_json_object':
        return 'invalid_json_object'

    elif test == '1/0':
        1/0

    #### apiphant.validation.field

    x = None

    if test == 'optional':
        x = field(request, 'x')

    elif test == 'default':
        x = field(request, 'x', default_value='X')

    elif test == 'required':
        x = field(request, 'x', is_required=True)

    elif test == 'valid_value':
        x = field(request, 'x', is_required=True, valid_value='X')

    elif test == 'valid_type':
        x = field(request, 'x', is_required=True, valid_type=int)

    elif test == 'valid_length':
        x = field(request, 'x', is_required=True, valid_length=2)

    elif test == 'max_length':
        x = field(request, 'x', is_required=True, max_length=2)

    #### Invalid

    if test == 'simple_invalid':
        raise Invalid('test')

    elif test == 'extended_invalid':
        raise Invalid('test', 'extended')

    #### ok

    return {"ok": True, "x": x}
