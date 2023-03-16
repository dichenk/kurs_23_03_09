from django.urls import path
from app_users.views import UsersLoginView, UsersCreateView, activate
from django.contrib.auth.views import LogoutView

app_name = 'app_users'


urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('register/', UsersCreateView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('signout/', LogoutView.as_view(), name='signout'),

]