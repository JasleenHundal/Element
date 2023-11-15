from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password', 'is_active', 'is_staff']  # Adjust fields as needed
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            role=validated_data['role'],
            is_active=validated_data.get('is_active', True),  # Defaulting to True if not provided
            is_staff=validated_data.get('is_staff', False)  # Defaulting to False if not provided
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Create a token for the new user
        Token.objects.create(user=user)

        return user
