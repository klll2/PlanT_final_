from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib.auth import get_user_model
from .models import Place, Plan, Trip, Route, Tag, Traveler
from django.views.decorators.csrf import csrf_exempt
import json, requests
# from django.core.serializers import serialize
# from datetime import date, timedelta, datetime
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView
# from google.auth.transport import requests
# from google.oauth2 import id_token
# from django.conf import settings
# Create your views here.
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .Q_learning.q_learning import GenerateTravelCourse
from .Q_learning.q_learning_query import RetrieveAndGenerate
from datetime import datetime, timedelta, date
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    TravelerSerializer, PlaceSerializer,
    TripSerializer, PlanSerializer, RouteSerializer, TagSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt  # jwt 모듈 임포트
from django.conf import settings  # settings 모듈 임포트
from django.shortcuts import get_object_or_404
# from .permission import IsAuthenticatedAndNotAdmin 
# from .authentication import CustomJWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TravelerFilter, TripFilter
from django.utils import timezone
import ast
from datetime import datetime
        
        
class TravelerListCreateView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny]
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TravelerFilter
    search_fields = ['trvlr_email']
    ordering_fields = ['trvlr_email']

class TravelerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    lookup_field = 'user_email'

# Trip Views
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TripFilter
    search_fields = ['trip_traveler']
    ordering_fields = ['trip_traveler']

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TripFilter
    search_fields = ['trip_traveler']
    ordering_fields = ['trip_traveler']

# Plan Views
class PlanListCreateView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class PlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

# Tag Views
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
# Place Views
class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

# Route Views
class RouteListCreateView(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data['mail']

        try:
            user = Traveler.objects.get(trvlr_email=email)
        except Traveler.DoesNotExist:
            # 존재하지 않는 사용자라면 새로 생성
            user = Traveler.objects.create(trvlr_email=email)
            
        current_time = timezone.now().date() + timedelta(days=1)
        for trip in Trip.objects.filter(trip_traveler=user.trvlr_id):
            if trip.trip_start <= current_time:
                if trip.trip_end <= current_time and trip.trip_start != trip.trip_end:
                    trip.trip_state = 3
                    trip.save()
                else:
                    trip.trip_state = 2
                    trip.save()
            else:
                trip.trip_state = 1
            trip.save(update_fields=['trip_state'])

        return Response({
            'id' : int(user.trvlr_id),
            'email' : str(user.trvlr_email)
        }, status=status.HTTP_201_CREATED)


class TripDelete(APIView):
    
    def post(self, request):
        trip_id = int(request.data.get('tripId'))
        
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response({'error': 'Invalid trip'}, status=400)
        
        trip.delete()
        
        return Response(status=status.HTTP_201_CREATED)       


def date_range(startdate, enddate):
    start_date = datetime.strptime(startdate, "%Y-%m-%d")
    end_date = datetime.strptime(enddate, "%Y-%m-%d")
    delta = timedelta(days=1)  # 날짜 간격 설정
    date_list = []
    
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += delta


# @csrf_exempt  
class Sender(APIView):
    
    def post(self, request):
        
        trip = request.data   

        trvlr = trip.get('trvlr_id')
        start_date_str = trip.get('start_date')
        end_date_str = trip.get('end_date')
        
        # if None in selected_tags:
        #     return Response({'error': 'Invalid date format. Expected YYYY-MM-DD'}, status=400)
        
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format. Expected YYYY-MM-DD'}, status=400)
        
        plan_count = (end_date - start_date).days + 1 
        date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(plan_count)]
        traveler = Traveler.objects.get(pk=trvlr)
        new_trip = Trip.objects.create(
            trip_start=start_date, 
            trip_end=end_date,
            trip_state=1,
            trip_traveler=traveler
        )
        
        if trip.get('selected_tags'):
            selected_tags = ast.literal_eval(trip.get('selected_tags'))
            method = "tag"
            tag_list = []
            for tag in selected_tags:
                try:
                    belong_tag = Tag.objects.get(pk=tag)
                    tags_id = belong_tag.tag_id
                except Tag.DoesNotExist:
                    return Response({'error': 'Invalid Tags'}, status=400)
                new_trip.trip_tags.add(tags_id)
                tag_list.append(tags_id)
            content = tag_list
        else:
            method = "query"
            content = trip.get('query')
            
        trip_info = [plan_count, date_list, new_trip.trip_id, method, content]
        plan_info = PlanMaker(trip_info)
        new_trip.trip_score = str(plan_info[1][3])
        new_trip.save(update_fields=['trip_score'])
        
        client_plans = {}
        if plan_info:
            for i in range(1,plan_count+1):
                place_list = []
                for j in range(len(plan_info[i][0])):
                    plc_name = Place.objects.get(pk=plan_info[i][0][j]).place_name  # 수정: plan_info[i][0][j]로 변경
                    place_list.append(plc_name)
                client_plans[i] = { "plc_ids" : plan_info[i][0],
                                 "plc_names" : place_list,
                                 "plc_times" : plan_info[i][1],
                                 "pln_score" : new_trip.trip_score,
                                 "q_1" : trip_info[0],
                                 "q_2" :trip_info[1] }
                
        return Response(client_plans, status=status.HTTP_201_CREATED)


def PlanMaker(trip_info):    
    
    plan_info = RetrieveAndGenerate(trip_info[0], trip_info[3], trip_info[4])
    
    # plan_info = []

    # if 2 in trip_info[1] and 4 in trip_info[1]:
    #     plan_info = { 1: [[2, 12, 1, 19, 26],
    #                     ['12:00', '12:05', '14:05', '14:07', '16:07', '16:09', '18:09', '18:13'],
    #                     [{'poi_id': 2, 'poi_name': '중앙시장', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 12, 'poi_name': '초당할머니순두부', 'arrival_time': '12:05', 'departure_time': '14:05'}, {'poi_id': 1, 'poi_name': '경포해변', 'arrival_time': '14:07', 'departure_time': '16:07'}, {'poi_id': 19, 'poi_name': '카페 툇마루', 'arrival_time': '16:09', 'departure_time': '18:09'}, {'poi_id': 26, 'poi_name': '씨마크호텔', 'arrival_time': '18:09', 'departure_time': None}],
    #                     "자연과 문화/역사를 골고루 둘러볼 수 있는 코스입니다. (87/100점, top 1)"]
    #                 }
    # elif 6 in trip_info[1]:

    #     plan_info = { 1: [[15, 21, 5, 28],
    #                      ['14:00', '14:08', '16:08', '16:09', '19:09', '19:25'],
    #                      [{'poi_id': 23, 'poi_name': '메밀라운지', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '12:08', 'departure_time': '14:08'}, {'poi_id': 21, 'poi_name': '예쁘다 하조대', 'arrival_time': '14:08', 'departure_time': '16:08'}, {'poi_id': 5, 'poi_name': '서피비치', 'arrival_time': '16:09', 'departure_time': '19:09'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '17:18', 'departure_time': '19:18'}],
    #                      "레저스포츠를 즐길 수 있는 코스입니다. (83/100점, top 1)"] 
    #                 }
    
    # else:
    #     plan_info = { 1: [[2, 12, 1, 19, 26],
    #                     ['12:00', '12:05', '14:05', '14:07', '16:07', '16:09', '18:09', '18:13'],
    #                     [{'poi_id': 2, 'poi_name': '중앙시장', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 12, 'poi_name': '초당할머니순두부', 'arrival_time': '12:05', 'departure_time': '14:05'}, {'poi_id': 1, 'poi_name': '경포해변', 'arrival_time': '14:07', 'departure_time': '16:07'}, {'poi_id': 19, 'poi_name': '카페 툇마루', 'arrival_time': '16:09', 'departure_time': '18:09'}, {'poi_id': 26, 'poi_name': '씨마크호텔', 'arrival_time': '18:09', 'departure_time': None}],
    #                     "자연과 문화/역사를 골고루 둘러볼 수 있는 코스입니다. (87/100점, top 1)"],
    #                  2: [[15, 21, 5, 28],
    #                     ['14:00', '14:08', '16:08', '16:09', '19:09', '19:25'],
    #                     [{'poi_id': 23, 'poi_name': '메밀라운지', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '12:08', 'departure_time': '14:08'}, {'poi_id': 21, 'poi_name': '예쁘다 하조대', 'arrival_time': '14:08', 'departure_time': '16:08'}, {'poi_id': 5, 'poi_name': '서피비치', 'arrival_time': '16:09', 'departure_time': '19:09'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '17:18', 'departure_time': '19:18'}],
    #                     "레저스포츠를 즐길 수 있는 코스입니다. (83/100점, top 1)"] 
    #                 }   
    
    if plan_info:
        i = 1
        
        for date in trip_info[1]:
            new_plan, created = Plan.objects.get_or_create(
                plan_date=date,
                plan_time = str(plan_info[i][1]),
                plan_trip = Trip.objects.get(pk=trip_info[2])
            )
            
            
            route_info = [new_plan.plan_id, plan_info[i][0], plan_info[i][1], plan_info[i][3], date]
            
            RouteMaker(route_info)
            
            i += 1
        
    return plan_info
    
    
def RouteMaker(route_info):
    
    i = 0
    
    while i+1 < len(route_info[1]):
        
        # starttime = combine_date_time(route_info[4], route_info[2][2*i])
        # endtime = combine_date_time(route_info[4], route_info[2][2*i+1])
        
        start_place = Place.objects.get(pk=route_info[1][i])
        end_place = Place.objects.get(pk=route_info[1][i + 1])
        new_route, created = Route.objects.get_or_create(
            # route_starttime=starttime,
            # route_endtime=endtime,
            route_start=start_place, 
            route_end=end_place,
            route_plan=Plan.objects.get(pk=route_info[0])
        )
        
        i += 1
        
    return True               
                    

class PlaceAddress(APIView):
    
    def post(self, request):
        
        trip = int(request.data.get('trip_id'))
        plans = Plan.objects.filter(plan_trip=trip).values_list('plan_id',flat=True)
        tags = Trip.objects.get(pk=trip).trip_tags
        score = Trip.objects.get(pk=trip).trip_score
        
        
        plc_address = {}
        i = 1
        
        for plan in plans:
            routes = Route.objects.filter(route_plan=int(plan))
                
            plc_ids = []
            for route in routes:
                plc_s = route.route_start.place_id
                plc_e = route.route_end.place_id
                if plc_s not in plc_ids:
                    plc_ids.append(plc_s)
                if plc_e not in plc_ids:
                    plc_ids.append(plc_e)
                        
            plc_names = []
            for plc in plc_ids:
                plc_name = Place.objects.get(pk=plc).place_name
                plc_names.append(plc_name)  
                    
            plan_time = Plan.objects.get(pk=int(plan)).plan_time
                    
            plc_address[i] = { 'plc_ids' : plc_ids,
                                'plc_names' : plc_names,
                                'plc_times' : plan_time.strip("[]").split(","),
                                'pln_score' : score
                            }
                
            i += 1
            
        return Response(plc_address, status=status.HTTP_201_CREATED)                
                
                    