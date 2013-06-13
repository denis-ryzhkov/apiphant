
#### status_by_code

status_by_code = {
    200: '200 OK',
    400: '400 Bad Request',
    403: '403 Forbidden',
    404: '404 Not Found',
    500: '500 Internal Server Error',
    501: '501 Not Implemented',
}

#### ApiError-s

class ApiError(Exception):
    def __init__(self, status_code, error=None):
        self.status_code = status_code
        self.error = error

class BadRequest(ApiError):
    def __init__(self, field_name, state, explain=None):
        super(BadRequest, self).__init__(400, '{field_name} is {state}'.format(field_name=field_name, state=state) + ('' if explain is None else ': {explain}'.format(explain=explain)))

class Missing(BadRequest):
    def __init__(self, field_name, explain=None):
        super(Missing, self).__init__(field_name, 'Missing', explain)

class Invalid(BadRequest):
    def __init__(self, field_name, explain=None):
        super(Invalid, self).__init__(field_name, 'Invalid', explain)

#### field

def field(request, field_name, is_required=False, default_value=None, valid_value=None, valid_type=None, valid_length=None, max_length=None, explain=None):

    if field_name not in request:
        if is_required:
            raise Missing(field_name, explain)
        return default_value

    field_value = request[field_name]

    if (
        valid_value is not None and field_value != valid_value or
        valid_type and not isinstance(field_value, valid_type) or
        valid_length is not None and len(field_value) != valid_length or
        max_length is not None and len(field_value) > max_length
    ):
        raise Invalid(field_name, explain)

    return field_value
