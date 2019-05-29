from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.serializer import LoginWithPhonePasswordSerializer
from user.views import LoginWithSmsCodeView, SmsCodeView, UserRegisterView, UserChangePasswordView

urlpatterns = [
    path('login/password/', TokenObtainPairView.as_view(serializer_class=LoginWithPhonePasswordSerializer),
         name='login_password'),
    path('login/code/', LoginWithSmsCodeView.as_view(), name='login_smscode'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('code/', SmsCodeView.as_view(), name='code'),
    path('register/', UserRegisterView.as_view(), name='register'),
    re_path(r'changepassword/(?P<pk>\d+)/', UserChangePasswordView.as_view(), name='change_password')
]
