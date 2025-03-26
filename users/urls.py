from django.urls import path
from .views import UserRegisterView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
