from django.urls import path
from .views import (
    Sender, LoginView,
    TravelerListCreateView, TravelerDetailView,
    TripListCreateView, TripDetailView,
    PlanListCreateView, PlanDetailView,
    TagListCreateView, TagDetailView,
    # TripTagListCreateView, TripTagDetailView,
    PlaceListCreateView, PlaceDetailView,
    RouteListCreateView, RouteDetailView,
    PlaceAddress, TripDelete,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)


urlpatterns = [ 
      # path('api/token/', TokenObtainPairView.as_view(), name='token'),
      # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
      # path('sender/', Sender),
      path('account/login/', LoginView.as_view(), name='google_login'),
      path('account/plans/new/', Sender.as_view(), name='new_plans'),
      path('account/plans/new/map/', PlaceAddress.as_view(), name='new_plans_map'),
      # path('account/logout/', LogoutView.as_view(), name='google_logout'),
      # path('account/state/', GoogleState, name='google_state'),
      # path('send/plans/', SendPlans, name='send_plans'),
      # path('output/trip/', TripMaker, name='output_trip'),
    # path('trip/', views.TripMaker),
    # path('route/', views.RouteMaker),
    # path('clust/', views.ClusterMaker),
    # path('plan/', views.Planner),
      path('api/travelers/', TravelerListCreateView.as_view(), name='traveler-list-create'),
      path('api/travelers/<int:pk>/', TravelerDetailView.as_view(), name='traveler-detail'),

      # Trip URLs
      path('api/trips/', TripListCreateView.as_view(), name='trip-list-create'),
      path('api/trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
      path('api/trips/delete/', TripDelete.as_view(), name='trip-delete'),
      
      # Plan URLs
      path('api/plans/', PlanListCreateView.as_view(), name='plan-list-create'),
      path('api/plans/<int:pk>/', PlanDetailView.as_view(), name='plan-detail'),

      # Tag URLs
      path('api/tags/', TagListCreateView.as_view(), name='tag-list-create'),
      path('api/tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),

      # TripTag URLs
      # path('api/trip-tags/', TripTagListCreateView.as_view(), name='triptag-list-create'),
      # path('api/trip-tags/<int:pk>/', TripTagDetailView.as_view(), name='triptag-detail'),

      # Place URLs
      path('api/places/', PlaceListCreateView.as_view(), name='place-list-create'),
      path('api/places/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),

      # Route URLs
      path('api/routes/', RouteListCreateView.as_view(), name='route-list-create'),
      path('api/routes/<int:pk>/', RouteDetailView.as_view(), name='route-detail'),
]