# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# import datetime
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils import timezone
# class CustomUserManager(BaseUserManager):
#     def create_user(self, user_email, password=None, **extra_fields):
#         if not user_email:
#             raise ValueError('The user_email field must be set')
#         user_email = self.normalize_email(user_email)
#         user = self.model(user_email=user_email, **extra_fields)
#         user.set_password(password)  # 패스워드 설정
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, user_email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('username', user_email)  # 변경: username을 user_email로 설정
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(user_email, password=password, **extra_fields)


# class User(AbstractUser):
#     user_email = models.EmailField(primary_key=True, unique=True)
    
#     def save(self, *args, **kwargs):
#         self.username = self.user_email  # user_email 값을 username에 할당
#         super().save(*args, **kwargs)
    
#     groups = models.ManyToManyField(Group, related_name='planT_Backend_user_groups')
#     permissions = models.ManyToManyField(Permission, related_name='planT_Backend_user_permissions')

#     USERNAME_FIELD = 'user_email'
#     REQUIRED_FIELDS = []
    
#     objects = CustomUserManager()


class Traveler(models.Model):
    trvlr_id = models.AutoField(primary_key=True)
    trvlr_email = models.EmailField(unique=True)


# class City(models.Model):
#     city_id = models.PositiveSmallIntegerField(primary_key=True)
#     city_name = models.CharField(max_length=10)
#     city_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    
class Tag(models.Model):
    tag_id = models.PositiveSmallIntegerField(primary_key=True)
    tag_name = models.CharField(max_length=20)
    

class Place(models.Model):
    place_id = models.PositiveIntegerField(primary_key=True)
    place_name = models.CharField(max_length=100)
    TYPE_CHOICES = (
        (1, '식사'),
        (2, '카페'),
        (3, '숙박'),
        (4, '관광'),
    )
    place_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    place_time = models.PositiveSmallIntegerField()
    place_latitude = models.DecimalField(max_digits=8, decimal_places=6)
    place_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # place_detail = models.JSONField(null=True, default=None)
    place_tags = models.ManyToManyField(Tag)


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_start = models.DateField()
    trip_end = models.DateField()
    STATE_CHOICES = (
        (1, '예정'),
        (2, '진행중'),
        (3, '완료'),
    )
    trip_state = models.PositiveSmallIntegerField(choices=STATE_CHOICES)
    trip_score = models.CharField(max_length=50, null=True)
    trip_traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    trip_tags = models.ManyToManyField(Tag)
        

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_date = models.DateField()
    plan_time = models.CharField(max_length=100, null=True)
    plan_trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    # route_starttime = models.DateTimeField(default=timezone.now)
    # route_endtime = models.DateTimeField(default=timezone.now)
    # route_detail = models.JSONField(blank=True, null=True, default=None)
    route_start = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='route_start_place')
    route_end = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='route_end_place')
    route_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
