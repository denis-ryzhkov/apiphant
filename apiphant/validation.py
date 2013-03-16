
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

class Invalid(ApiError):

    def __init__(self, field_name):
        super(Invalid, self).__init__(400, '{field_name} is Invalid'.format(field_name=field_name))

#### field

def field(request, field_name, is_required=False, default_value=None, valid_value=None, valid_type=None, valid_length=None):

    if field_name not in request:
        if is_required:
            raise ApiError(400, '{field_name} is Missing'.format(field_name=field_name))
        return default_value

    field_value = request[field_name]

    if (
        valid_value is not None and field_value != valid_value or
        valid_type and not isinstance(field_value, valid_type) or
        valid_length is not None and len(field_value) != valid_length
    ):
        raise Invalid(field_name)

    return field_value
