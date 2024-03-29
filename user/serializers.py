from rest_framework import serializers
from django.contrib.auth import authenticate

from user.models import User, Profile



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class UserRegistrySerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: 'Password doesn\'t match'})
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user']

    @staticmethod
    def get_user(obj):
        return obj.user.username if not (obj.user.first_name and obj.user.last_name) else ' '.join([obj.user.first_name, obj.user.last_name])