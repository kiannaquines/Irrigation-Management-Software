from django.urls import path
from .views import RegisterView,LoginView,logout_view,PasswordResetView,SetNewPasswordView

urlpatterns = [
    path("",LoginView.as_view(),name="login"),
    path("register/",RegisterView.as_view(),name="register"),
    path("logout/",logout_view,name="logout"),
    path("password-reset/",PasswordResetView.as_view(),name="reset"),
    path("set-password/<str:email>/<str:mobile>/",SetNewPasswordView.as_view(),name="new_password"),
]
