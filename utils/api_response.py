from rest_framework.response import Response


class ApiResponse:

    @staticmethod
    def success(message=None, data=None, status_code=200, template_name=None, headers=None, content_type='application/json'):
        return Response({
                "status": 1,
                "message": message,
                "data": data
            }, status_code, template_name, headers, content_type)
    

    @staticmethod
    def error(message=None, status_code=200, template_name=None, headers=None, content_type='application/json'):
        return Response({
            "status": 0,
            "message": message
        }, status_code, template_name, headers, content_type)
    

    @staticmethod
    def non_fields_error_response(message=None, status_code=400, template_name=None, headers=None, content_type='application/json'):
        return Response({
            "status": 0,
            "errors": {
                "non_fields_errors": [message]
            }
        }, status_code, template_name, headers, content_type)
