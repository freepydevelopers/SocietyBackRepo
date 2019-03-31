from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = errors
        response.data['status'] = False

        response.data['exception'] = str(exc)

    return response

class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_an_error_response = True
    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message
    def to_dict(self):
        return {'errorMessage': self.error_message}

class InvalidUsage(BaseCustomException):
    status_code = 400
