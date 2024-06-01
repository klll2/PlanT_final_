from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib.auth import get_user_model
from .models import Place, Plan, Trip, Route, Tag, TripTag, Traveler
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
from datetime import datetime, timedelta, date
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    TravelerSerializer, TripTagSerializer, PlaceSerializer,
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

class LoginView(APIView):
    def post(self, request):
        email = request.data['mail']

        try:
            user = Traveler.objects.get(trvlr_email=email)
        except Traveler.DoesNotExist:
            # 존재하지 않는 사용자라면 새로 생성
            user = Traveler.objects.create(trvlr_email=email)

        return Response({
            'id' : int(user.trvlr_id),
            'email' : str(user.trvlr_email)
        }, status=status.HTTP_201_CREATED)
        
        
        
        
# class LogoutView(APIView):
    
#     def post(self, request):
#         try:

#             # Authorization 헤더에서 토큰 추출
#             token = request.headers['Authorization'].split()[1]

#             # 토큰 블랙리스트에 추가하여 무효화
#             refresh_token = RefreshToken(token)
#             refresh_token.blacklist()

#             return Response({"success": "Logged out successfully."}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def MyTripsView(request):
#     # HTTP 요청의 헤더에서 이메일 값을 가져옵니다.
#     user_email = request.headers.get('X-User-Email', None)

#     if user_email:
        
#         trips = Trip.objects.filter(trip_user=user_email)  # 해당 사용자의 여행 정보 필터링
#         serializer = TripSerializer(trips, many=True)  # 시리얼라이즈

#         return Response(serializer.data)
    
#     else:
#         # 이메일 값이 없는 경우 처리
#         return Response({'error': 'No email provided'}, status=status.HTTP_400_BAD_REQUEST)
    

# class MyTripsView(APIView):
    
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         if not user:
#             return Response({"error": "User not found"}, status=404)

#         trips = Trip.objects.filter(trip_user=user.user_email)  # 해당 사용자의 여행 정보 필터링
#         serializer = TripSerializer(trips, many=True)  # 시리얼라이즈

#         return Response(serializer.data)


# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

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

# TripTag Views
class TripTagListCreateView(generics.ListCreateAPIView):
    queryset = TripTag.objects.all()
    serializer_class = TripTagSerializer

class TripTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TripTag.objects.all()
    serializer_class = TripTagSerializer 
    
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


@csrf_exempt
@api_view(['POST'])
def GoogleLogin(request):
    if request.method == 'POST':
        # 리액트 애플리케이션에서 전송한 토큰 받기
        token = request.POST.get('token')

        # 토큰 검증 및 사용자 정보 얻기
        user_info = verify_google_token(token)

        if user_info:
            # 사용자 정보에서 이메일 추출
            email = user_info.get('email')
            user, created = User.objects.get_or_create(user_email=email)
            
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_email': email
            })
        else:
            return JsonResponse({'error': 'Invalid token'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



def verify_google_token(token):
    # 여기에는 Google 토큰을 검증하고 사용자 정보를 반환하는 코드가 들어갑니다.
    # 예를 들어, Google API를 사용하여 토큰을 검증하고 사용자 정보를 얻을 수 있습니다.
    # 이 코드는 Google 로그인 및 토큰 검증에 관한 문서를 참조하여 작성해야 합니다.
    # 예시로는 requests를 사용하여 Google API에 요청하는 방법을 보여드리겠습니다.
    
    # Google API에 토큰 검증 요청 보내기
    response = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': token})

    if response.status_code == 200:
        # 요청이 성공하면 사용자 정보 반환
        return response.json()
    else:
        # 요청이 실패하면 None 반환
        return None


@api_view(['POST'])
def GoogleLogout(request):
    if request.method == 'POST':
        # 로그아웃 요청 처리
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def GoogleState(request):
    if request.method == 'POST':
        if request.session:
            user_email = request.session.get('user_email')
        else:
            user_email = ""
        return Response(user_email, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @csrf_exempt
# def sender(request):
#     city = City.objects.all().values_list("city_name", flat=True)
# #    plc1 = Place.objects.all().values_list("city_id", flat=True)
# #    plc2 = Place.objects.all().values_list("city_id", flat=True)
# #    Plan = City.objects.all().values_list("city_id", flat=True)
    
#     return JsonResponse(list(city), safe=False)


# @csrf_exempt
# def reciever(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))  # JSON 데이터를 파이썬 객체로 변환
#         option_value = data.get('ops')
#         if option_value:
#             option = str(option_value)
#             cid = City.objects.get(city_name=option)
#             option = Place.objects.filter(city=cid).values_list('place_id','place_name')
#             dict = {}
#             for i in option:
#                 dict[i[0]] = i[1]
#             #serialized_option = serialize('json', option, fields=('place_name',))
#             return JsonResponse(dict, safe=False)
#         else:
#             return JsonResponse({'error': 'Option value is required'}, status=400)
        
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer


# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         '/api/token/',
#         '/api/register/',
#         '/api/token/refresh/'
#     ]
#     return Response(routes)


#class recommender:
#    def __init__(self, ):


# def Filter(table, filter_dict, use_fields):
    
#     if not filter_dict:
#         filtered_objects = table.objects.values(*use_fields)
    
#     filtered_objects = table.objects.filter(**filter_dict).values(*use_fields)   
#     return filtered_objects


# # @csrf_exempt        
# class Sender(APIView):
    
#     def post(self, request):
        
#         trip_info = request.data

        
            
#         if fields != 'all':
#             values = data.get('values')
#             filter_dict = dict(zip(fields, values))
        
        
#         if table and fields:
            
#             if table == 'tag' and fields == 'all': # 전체 태그
#                 send = Tag.objects.values('tag_id', 'tag_name')
                
#             # elif table== 'city': # 도시 필터링
#             #     use_fields = ['city_id', 'city_name'] 
#             #     send = Filter(City, filter_dict, use_fields)

#             elif table == 'place': # 장소 필터링
#                 use_fields = ['place_id', 'place_name']
#                 send = Filter(Place, filter_dict, use_fields)
                
#                 if data.get("selected_plc"): # 선택된 장소 제외 필터링
#                     selected_plc = data.get("selected_plc")
#                     poss_plc = Place.objects.exclude(id__in = selected_plc)
#                     send = Filter(poss_plc, filter_dict, use_fields)
                    
#             elif table == 'route': # 루트 필터링
#                 use_fields = ['route_id','route_time', 'route_co2']
#                 send = Filter(Route, filter_dict, use_fields) # route_plan = plan_id
            
#             elif table == 'detail_route': # 상세 루트 정보
#                 route = data.get('route')
#                 send = {
#                     'rount_startplc' : Route.objects.get(pk=route).route_start,
#                     'rount_endplc' : Route.objects.get(pk=route).route_end,
#                     'rount_starttime' : Route.objects.get(pk=route).route_start,
#                     'rount_endtime' : Route.objects.get(pk=route).route_end,
#                 }
#                 # send['rount_startplc'] = Route.objects.get(pk=route).route_start  
#                 # send['rount_endplc'] = Route.objects.get(pk=route).route_end
#                 # send['rount_starttime'] = Route.objects.get(pk=route).route_start  
#                 # send['rount_endtime'] = Route.objects.get(pk=route).route_end
                
                
#             return JsonResponse(send, safe=False)
        
#         else:
#             return JsonResponse({'error': 'value is required'}, status=400)



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
# def SendPlans(request):
#     if request.method == 'GET':
#         data = request.session.get("client_plans")
#         return JsonResponse(data)
#         # if data:
#         #     return JsonResponse(data)
#         # else:
#         #     return JsonResponse({'error': 'Session Expiration. Please Login again'}, status=403)
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed.'}, status=400)
 
 
# @csrf_exempt  
# def SendTrips(request):
#     if request.method == 'GET':
#         email = request.session.get("user_email")
#         trips = Trip.objects.filter(trip_user=email)
#         data = []
#         for trip in trips:
#             tag_list = trip.trip_tag.all()
#             tag_namelist = [tag.tag_name for tag in tag_list]
#             data.append( 
#                         {"trip_start" : trip.trip_start, 
#                            "trip_end" : trip.trip_end, 
#                            "trip_tag" : tag_namelist, 
#                          "trip_state" : trip.trip_state }
#                         )
        
#         if data:
#             return JsonResponse(data, safe=False)
#         else:
#             return JsonResponse({'error': 'Session Expiration. Please Login again'}, status=403)
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed.'}, status=400)    
   
    
# @csrf_exempt  
# def TripMaker(request):    
    
#     if request.method == 'POST':
#         start_date = "2024-05-22"
#         end_date = "2024-05-22"
#         selected_tags = ["바다여행","시장투어"]
#         plan_count = 1
#         date_list = ["2024-05-22"]
        
#         if request.session:
#             email = request.session.get('user_email')
#             new_trip = Trip(trip_start = start_date, 
#                             trip_end = end_date,
#                             trip_state = 1,
#                             trip_user = User.objects.all()[1])
#             new_trip.save()
            
#             tag_list = []
            
#             for tag in selected_tags:
#                 belong_tag = Tag.objects.get(tag_name=tag)
#                 tag_list.append(belong_tag.tag_id)
#                 TripTag.objects.create(trip=new_trip, tag=belong_tag)
        
#             trip_info = [plan_count, tag_list, date_list, new_trip.trip_id]
            
#             plan_info = PlanMaker(trip_info)
            
#             client_plans = {}
            
#             if plan_info:
                
#                 for i in range(1,plan_count+1):
#                     place_list = []
#                     for j in range(len(plan_info[i][0])):
#                         plc_name = plan_info[i][2][j]['poi_name']
#                         place_list.append(plc_name)
                    
#                     client_plans[i] = [place_list,
#                                        plan_info[i][1],
#                                        plan_info[i][3]]
                    
#             request.session['client_plans'] = client_plans
                    
#             return JsonResponse({"Success":"Success"})
            
#         else:
#             return JsonResponse({'error': 'Session Expiration. Please Login again'}, status=403)
        
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed.'}, status=400)
    
# @csrf_exempt      
@api_view(['GET'])
def SendPlans(request):
    if request.method == 'GET':
        data = request.session.get("client_plans")
        return Response(data)
    else:
        return Response({'error': 'Only GET requests are allowed.'}, status=400)
 
# @csrf_exempt  
@api_view(['GET'])
def SendTrips(request):
    if request.method == 'GET':
        # email= User.objects.all()[1]
        # login(request, email)
        user_mail = request.session.get("user_email")
        # email = request.session.get("user_email")
        trips = Trip.objects.filter(trip_user=user_mail)
        data = []
        for trip in trips:
            tag_list = trip.trip_tag.all()
            tag_namelist = [tag.tag_name for tag in tag_list]
            data.append({ 
                "trip_start" : trip.trip_start, 
                "trip_end" : trip.trip_end, 
                "trip_tag" : tag_namelist, 
                "trip_state" : trip.trip_state 
            })
        if data:
            return Response(data)
        else:
            return Response({'error': 'Session Expiration. Please Login again'}, status=403)
    else:
        return Response({'error': 'Only GET requests are allowed.'}, status=400)    
    

# @csrf_exempt  
class Sender(APIView):
    
    def post(self, request):
        
        trip = request.data   

        trvlr = trip.get('trvlr_id')
        start_date_str = trip.get('start_date')
        end_date_str = trip.get('end_date')
        selected_tags = trip.get('selected_tags')
        
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format. Expected YYYY-MM-DD'}, status=400)
        
        plan_count = 1
        date_list = [start_date_str]
        traveler = Traveler.objects.get(pk=trvlr)
        new_trip, created = Trip.objects.get_or_create(
            trip_start=start_date, 
            trip_end=end_date,
            trip_state=1,
            trip_traveler=traveler
        )
        tag_list = []
        for tag in selected_tags:
            belong_tag = Tag.objects.get(pk=tag)
            tag_list.append(tag)
            TripTag.objects.get_or_create(trip=new_trip, tag=belong_tag)
        trip_info = [plan_count, tag_list, date_list, new_trip.trip_id]
        plan_info = PlanMaker(trip_info)
        client_plans = {}
        if plan_info:
            for i in range(1,plan_count+1):
                place_list = []
                for j in range(len(plan_info[i][0])):
                    plc_name = plan_info[i][2][j]['poi_name']
                    place_list.append(plc_name)
                client_plans = { "plc_names" : place_list,
                                 "plc_times" : plan_info[i][1],
                                 "pln_score" : plan_info[i][3]}
        return Response(client_plans, status=status.HTTP_201_CREATED)
    


def PlanMaker(trip_info):    
    
    # plan_info = GenerateTravelCourse(trip_info[0],trip_info[1])
    
    plan_info = { 1: [[2, 12, 1, 19, 26],
                    ['12:00', '12:05', '14:05', '14:07', '16:07', '16:09', '18:09', '18:09'],
                    [{'poi_id': 2, 'poi_name': '중앙시장', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 12, 'poi_name': '초당할머니순두부', 'arrival_time': '12:05', 'departure_time': '14:05'}, {'poi_id': 1, 'poi_name': '경포해변', 'arrival_time': '14:07', 'departure_time': '16:07'}, {'poi_id': 19, 'poi_name': '카페 툇마루', 'arrival_time': '16:09', 'departure_time': '18:09'}, {'poi_id': 26, 'poi_name': '씨마크호텔', 'arrival_time': '18:09', 'departure_time': None}],
                    "바다 여행 : 20, 시장 투어 : 20"]
                }

# {
#     1:  
# 		[[23, 18, 21, 5, 18],
#         ['12:00', '12:08', '14:08', '14:08', '16:08', '16:09', '19:09', '17:18', '19:18'],
#         [{'poi_id': 23, 'poi_name': '메밀라운지', 'arrival_time': '10:00', 'departure_time': '12:00'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '12:08', 'departure_time': '14:08'}, {'poi_id': 21, 'poi_name': '예쁘다 하조대', 'arrival_time': '14:08', 'departure_time': '16:08'}, {'poi_id': 5, 'poi_name': '서피비치', 'arrival_time': '16:09', 'departure_time': '19:09'}, {'poi_id': 18, 'poi_name': '싱글핀 에일웍스', 'arrival_time': '17:18', 'departure_time': '19:18'}],
#         {5: 20}] 
# }
    
    
    i = 1
    
    for date in trip_info[2]:
        new_plan, created = Plan.objects.get_or_create(
            plan_date=date,
            plan_trip=Trip.objects.get(pk=trip_info[3])
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
            route_start=start_place,
            route_end=end_place,
            route_plan=Plan.objects.get(pk=route_info[0])
        )
        
        i += 1
        
    return True

    
# def combine_date_time(date_str, time_str):
#     """
#     Combine a date string and a time string into a datetime object.

#     :param date_str: A string representing the date in 'YYYY-MM-DD' format.
#     :param time_str: A string representing the time in 'HH:MM' format.
#     :return: A datetime object representing the combined date and time.
#     """
#     # Define the format of the date and time strings
#     date_format = "%Y-%m-%d"
#     time_format = "%H:%M"
    
#     # Parse the date and time strings into datetime objects
#     date_part = datetime.strptime(date_str, date_format)
#     time_part = datetime.strptime(time_str, time_format)
    
#     # Combine the date and time parts into a single datetime object
#     combined_datetime = datetime.combine(date_part, time_part.time())
    
#     return combined_datetime   

#     if request.method == 'POST':
        
#         data = json.loads(request.body.decode('utf-8'))  # JSON 데이터를 파이썬 객체로 변환
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         move_date = data.get('move_date')
#         from_city = data.get('from_city')
#         to_city = data.get('to_city')
        
#         new_trip = Trip(trip_start = start_date, 
#                         trip_end = end_date,
#                         trip_state = 1,
#                         trip_ecolevel = data.get('poss_time'),
#                         trip_posstime = data.get('eco_lev'),
#                         trip_user = 'user1')
        
#         new_trip.save()
        
#         current_date = start_date
        
#         plan_count = (end_date - start_date).days 
#         plc_count = plan_count * 2 # 고를 수 있는 장소 수
    
#         stay_city = from_city
#         plan_list = []
#         move_city_list = [stay_city]
        
#         for i in range(plan_count + 1):
               
#             if current_date > move_date:
#                 stay_city = to_city
#                 move_city = to_city
#                 move_plan = 1
#                 if new_plan:
#                     move_plan = new_plan.plan_id
#                 plc_count -= 2
#                 move_plan_index = i+1          

#             new_plan = Plan(plan_date = current_date,
#                             plan_trip = new_trip.trip_id,
#                             plan_city = stay_city)
            
#             new_plan.save()
#             plan_list.append(new_plan.plan_id)
#             current_date += timedelta(days=1)
            
#             move_city_list.append(move_city)
        
#         return JsonResponse({'message': 'New trip is created with plans',
#                              'move_plan': move_plan,
#                              'move_plan_index' : move_plan_index,
#                              'move_city_list' : move_city_list,
#                              'plan_list' : plan_list,
#                              'plc_count' : plc_count},
#                             safe=False)
        
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)     
 

# def RouteMaker(request):
    
#     if request.method == 'POST':
        
#         data = json.loads(request.body.decode('utf-8'))
#         start_plc = data.get('start_plc')
#         end_plc = data.get('end_plc')
#         move_plan = data.get('move_plan')
        
#         origin_date = Plan.objects.get(pk=move_plan).plan_date

#         new_route = Route(route_type = 3,
#                           route_transport = 3,
#                           route_starttime = origin_date.replace(hour=8, minute=0, second=0, microsecond=0),
#                           route_endtime = origin_date.replace(hour=23, minute=0, second=0, microsecond=0),
#                           route_time = 15,
#                           route_co2 = 0,
#                           route_detail = None,
#                           route_start = start_plc,
#                           route_end = end_plc,
#                           route_plan = move_plan)
        
#         new_route.save()
        
#         return JsonResponse({'message': 'New move plan is created'}, safe=False)
        
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)  


# def ClusterMaker(request):
     
#     if request.method == 'POST':
        
#         data = json.loads(request.body.decode('utf-8'))
#         plc_list = data.get('plc_list')
#         cluster_count = data.get('clst_count')
        
#         plc_dict = {}
        
#         return JsonResponse(plc_dict, safe=False)
        
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
    

# def PlanClassifier(request):
    
#     if request.method == 'POST':
        
#         data = json.loads(request.body.decode('utf-8'))
#         plan_dict = data.get('plan_dict')
        
    
#         tag_list = Tag.objects.values_list('tag_id', flat=True)
#         tag_dict = {}
        
#         for tag in tag_list:
#             tag_dict[tag] = 0
                
#         for i in range(1,len(plan_dict)+1):
            
#             for j in plan_dict[i]:
                
#                 if j in tag_list:
#                     tag_dict[j] += 1
                    
                
        
#         return plan_dict, plc, pln 
    
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)   
          
            
# def AssignTag(eco_lev, tag_dict):

#     if eco_lev == 0:
#         tag_per = 0
        
#     elif eco_lev == 1:
#         tag_per = 20
        
#     elif eco_lev == 2:
#         tag_per = 40
        
#     elif eco_lev == 3:
#         tag_per = 60
        
#     elif eco_lev == 4:
#         tag_per = 80
        
#     else:
#         tag_per = 100
        
#     for i in tag_dict:
#         tag_dict[i] /= tag_per
        
#     return tag_dict


# def Coordinate(plc_id):
    
#     plc = Place.objects.get(pk=plc_id)
        
#     return (plc.place_latitude, plc.place_longitude)
             
            
# def Planner(request):
    
#     if request.method == 'POST':
        
#         data = json.loads(request.body.decode('utf-8'))
#         plan_dict = data.get('plan_dict')
#         tag_dict = data.get('tag_dict')
#         eco_lev = Plan.objects.get(pk=plan_dict[1][0]).plan_trip.trip_ecolevel
#         tag_dict = AssignTag(eco_lev, tag_dict)
    
#         i, j = 1, 0
        
#         while i <= len(plan_dict) and j < len(plan_dict[i][1]):
            
#             convex_hull = [Coordinate(k) for k in plan_dict[i][1] if k >= 10]
                    
#             if plan_dict[i][1][j] - 10 < 0:
#                 city = Plan.objects.get(pk=plan_dict[i][0]).plan_city.city_id
#                 place_set = Place.objects.filter(place_city=city, place_tag=plan_dict[i][1][j]).values_list('place_id', flat=True)
                
#                 input = {1 : plan_dict[i][1][j-1], # 출발지
#                          2 : convex_hull, # 폴리곤 만드는데 사용되어야 할 좌표들(위도, 경도), 해당 일정에서 특정된 장소들, 만약 1개라면 num1_in_out 사용하도록
#                          3 : place_set} # 해당 지역, 해당 태그로 1차 필터링된 장소들(in_out의 대상)
                
#                 # input 보내서 접근 가능한 장소(id) 리스트로 받아오기
#                 # plc_poss = in_out(input)
#                 plc_poss = Place.objects.filter(place_tag = plan_dict[i][j]) # 나중에 받으면 교체
                        
#                 # 친환경 레벨에 해당하는 비율만큼 할당된 경우 일반 장소로만 추천, 남아있으면 친환경 장소로만 추천
#                 plc_poss_eco = [plc for plc in plc_poss if Place.objects.get(pk=plc).place_eco]
#                 plc_poss_noneco = [plc for plc in plc_poss if not Place.objects.get(pk=plc).place_eco]
#                 eco_state = 0
                
#                 if tag_dict[plan_dict[i][1][j]] > 0 and plc_poss_eco:
                    
#                     tag_dict[plan_dict[i][1][j]] -= 1
#                     eco_state = 1
                    
#                 coordinated_plc_poss = [Coordinate(plc) for plc in plc_poss_noneco]
                
#                 input = {1 : Coordinate(plan_dict[i][1][j-1]), # 출발지 좌표(x,y)
#                          2 : coordinated_plc_poss, # 목적지 후보들 좌표(x,y) 리스트
#                          3 : plc_poss_noneco} # 목적지 후보들 id(위 좌표 리스트와 순서쌍)
                
#                 if eco_state:
#                     coordinated_plc_poss_eco = [Coordinate(plc) for plc in plc_poss_eco]
                    
#                     input_eco = {1 : Coordinate(plan_dict[i][1][j-1]), # 출발지 좌표(x,y)
#                                 2 : coordinated_plc_poss_eco, # 목적지 후보들 좌표(x,y) 리스트
#                                 3 : plc_poss_eco} # 목적지 후보들 id(위 좌표 리스트와 순서쌍)
                    
#                     eco_route_info = 1
                    
#                     last_route_id = Route.objects.values_list('route_id',flat=True).order_by('-route_id')[0]
#                     new_route_id_eco = last_route_id + 1
                    
#                     last_plan_route = Route.objects.filter(route_plan=plan_dict[i][0]).values_list('route_id',flat=True)
                    
#                     if last_plan_route:
#                         last_plan_route_id = last_plan_route.order_by('-route_id')[0]
#                         start_time = Route.objects.get(pk=last_plan_route_id).route_endtime
                    
#                     else:
#                         start_time = Plan.objects.get(pk=plan_dict[i][0]).plan_date + datetime.timedelta(hours=8, minutes=0, seconds=0, microseconds=0)
                    
#                     end_time = start_time + timedelta(minutes=eco_route_info[2])
                
#                 # 루트 플랜에 저장하기
#                     new_route_eco = Route(route_type = 1,
#                                           route_transport = eco_route_info[1],
#                                           route_starttime = start_time,
#                                           route_endtime = end_time,
#                                           route_time = eco_route_info[2],
#                                           route_co2 = eco_route_info[3],
#                                           route_detail = None,
#                                           route_start = plan_dict[i][1][j],
#                                           route_end = eco_route_info[0],
#                                           route_plan = plan_dict[i][0])
                
#                     new_route_eco.save()
                    
#                 # 보내서 최단거리 장소(id),이동수단,소요시간,탄소배출량 받기
#                 route_info = 1
#                 plc_id = 11
#                 plc_move = 3
#                 plc_time = 30
#                 plc_co2 = 30 # 정해지면 지우기
                
#                 # 루트 플랜에 저장하기
#                 last_plan_route = Route.objects.filter(route_plan=plan_dict[i][0]).values_list('route_id',flat=True)
                    
#                 if last_plan_route:
#                     last_plan_route_id = last_plan_route.order_by('-route_id')[0]
#                     start_time = Route.objects.get(pk=last_plan_route_id).route_endtime
                    
#                 else:
#                     start_time = Plan.objects.get(pk=plan_dict[i][0]).plan_date + datetime.timedelta(hours=8, minutes=0, seconds=0, microseconds=0)
                    
#                 end_time = start_time + timedelta(minutes=route_info[2])
                
#                 # 루트 플랜에 저장하기
#                 new_route = Route(route_type = 2,
#                                   route_transport = route_info[1],
#                                   route_starttime = start_time,
#                                   route_endtime = end_time,
#                                   route_time = route_info[2],
#                                   route_co2 = route_info[3],
#                                   route_detail = None,
#                                   route_start = plan_dict[i][1][j],
#                                   route_end = route_info[0],
#                                   route_plan = plan_dict[i][0])
            
#                 new_route.save()
                
#             else: # 장소 -> 장소(지정경로)  
                
#                 confirmed_route_info = APIRoute(Coordinate(plan_dict[i][1][j-1]), Coordinate(plan_dict[i][1][j]))  
                
#                 last_route_id = Route.objects.values_list('route_id',flat=True).order_by('-route_id')[0]
#                 new_confirmed_route_id = last_route_id + 1
                    
#                 last_plan_route = Route.objects.filter(route_plan=plan_dict[i][0]).values_list('route_id',flat=True)
                    
#                 if last_plan_route:
#                     last_plan_route_id = last_plan_route.order_by('-route_id')[0]
#                     start_time = Route.objects.get(pk=last_plan_route_id).route_endtime
                    
#                 else:
#                     start_time = Plan.objects.get(pk=plan_dict[i][0]).plan_date + datetime.timedelta(hours=8, minutes=0, seconds=0, microseconds=0)
                    
#                 end_time = start_time + timedelta(minutes=confirmed_route_info[2])
                
#                 # 루트 플랜에 저장하기
#                 new_confirmed_route = Route(route_id = new_confirmed_route_id,
#                                             route_type = 3,
#                                             route_transport = confirmed_route_info[1],
#                                             route_starttime = start_time,
#                                             route_endtime = end_time,
#                                             route_time = confirmed_route_info[2],
#                                             route_co2 = confirmed_route_info[3],
#                                             route_detail = None,
#                                             route_start = plan_dict[i][1][j-1],
#                                             route_end = plan_dict[i][1][j],
#                                             route_plan = plan_dict[i][0])
            
#                 new_confirmed_route.save()    
                            
#             j += 1 
                    
#             if j == len(plan_dict[i][1]): # 해당 일자의 장소가 모두 정해지면 다음 장소로 변경

#                 j = 0
#                 i += 1
        
#         trip = Plan.objects.get(pk=plan_dict[0][0]).plan_trip.trip_id
#         plans_list = Plan.objects.filter(plan_trip=trip).values_list('plan_id', flat=True).order_by('plan_id')
                
#         return JsonResponse(plans_list, safe=False)
        
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)        
                
                    
                    