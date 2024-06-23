from rest_framework import serializers
from account.models import User
from utils.constants import PASSWORD_NOT_MATCHED

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
