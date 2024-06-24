from rest_framework import serializers
from account.models import User
from utils.constants import PASSWORD_NOT_MATCHED
#for the send password reset link in email
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}
                                      ,write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2','tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    #validate password and confirm password during registration and validate is inbuild method in python.
    def validate(self, attrs):
        passwords = attrs.get('password')
        password2 = attrs.get('password2')

        if passwords!= password2:
            raise serializers.ValidationError(
                PASSWORD_NOT_MATCHED
            )
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password'] 


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']



class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    class Meta:
        fiels = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password!= password2:
            raise serializers.ValidationError(
                PASSWORD_NOT_MATCHED
            )
        user.set_password(password)
        user.save()
        return attrs
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("uid: %s" % uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("token: %s" % token)
            link = f"https://localhost:3000/api/v1/users/reset_password/{uid}/{token}"
            print("link: %s" % link)
            # Here, you can send the email containing the reset link to the user
            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist."
            )



