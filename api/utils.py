from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first.
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data.
        response.data['status_code'] = response.status_code
        response.data['detail'] = response.data.get('detail', 'An error occurred.')

    return response
