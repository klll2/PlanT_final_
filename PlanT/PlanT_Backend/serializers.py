# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Place, Plan, Trip, Route, Tag, Traveler


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = ['trvlr_id', 'trvlr_email']


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'trip_start', 'trip_end', 'trip_state', 'trip_score', 'trip_traveler', 'trip_tags']



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['plan_id', 'plan_date', 'plan_time', 'plan_trip']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_id', 'tag_name']


# class TripTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TripTag
#         fields = ['trip', 'tag']


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_id', 'place_name', 'place_type', 'place_time', 'place_latitude', 'place_longitude', 'place_tags']



class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'route_start', 'route_end', 'route_plan']


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethodwe
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
#         token['username'] = user.username
#         token['email'] = user.email
#         return token


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['user id']
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         Users.objects.create(
#             user_id=validated_data['user id'],
#         )

