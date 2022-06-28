from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.LoginView.as_view(authentication_form=views.CustomLoginForm), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.SignupView.as_view(), name="signup"),
]