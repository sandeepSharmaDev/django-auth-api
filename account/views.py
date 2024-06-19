from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer
from utils.api_response import ApiResponse
from utils.constants import SUCCESS_USER_REGISTERED,INVALID_PASSWORD,USER_LOGIN_SUCCESS
from account.serializers import UserLoginSerializer
from django.contrib.auth import authenticate


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return ApiResponse.success(
                message=SUCCESS_USER_REGISTERED,
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return ApiResponse.error(
            message=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            # authenticate is the method that use for authenticating the user
            authenticate(email=email, password=password)
            user = authenticate(email=email, password=password)

            if user is not None:
                return ApiResponse.success(
                    message=USER_LOGIN_SUCCESS,
                    data=serializer.data,
                    status_code=status.HTTP_200_OK)
            else:
                return ApiResponse.non_fields_error_response(
                    message= INVALID_PASSWORD)

        return ApiResponse.error(message=serializer.errors,
                                status_code=status.HTTP_400_BAD_REQUEST)

