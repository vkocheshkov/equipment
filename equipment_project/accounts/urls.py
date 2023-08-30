from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginAPIView, LogoutAPIView

# from rest_framework_simplejwt.views import TokenRefreshView
#
# from accounts.views import LoginAPIView, LogoutAPIView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]