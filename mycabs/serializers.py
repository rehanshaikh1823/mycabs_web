from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import MinValueValidator, MaxValueValidator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'error': 'Invalid username or password'})
        attrs['user'] = user
        return attrs


# class LocationUpdateSerializer(serializers.Serializer):
#     latitude = serializers.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     longitude = serializers.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

class LocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    address = serializers.CharField(required=False, allow_blank=True)