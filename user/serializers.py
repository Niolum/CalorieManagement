from rest_framework import serializers

from user.models import User, Profile



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user']