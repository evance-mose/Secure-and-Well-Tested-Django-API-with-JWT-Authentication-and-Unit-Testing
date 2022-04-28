from django.urls import path
from api import views as api_views
from rest_framework.authtoken import views as token_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('customers/', api_views.CustomerView.as_view(), name='customer'),
    path('customers/<int:pk>/', api_views.CustomerDetailView.as_view(),
         name='customer-detail'),
    path('api-token-auth/', token_views.obtain_auth_token, name='api-token-auth'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
