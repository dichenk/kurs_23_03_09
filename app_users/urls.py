from django.urls import path
from app_users.views import UsersLoginView, UsersCreateView, activate, ManagersUserListView, change_user_status
from django.contrib.auth.views import LogoutView

app_name = 'app_users'


urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('users/', ManagersUserListView.as_view(), name='users'),
    path('change_user_status/<int:pk>/', change_user_status, name='change_user_status'),
    path('register/', UsersCreateView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('signout/', LogoutView.as_view(), name='signout'),

]