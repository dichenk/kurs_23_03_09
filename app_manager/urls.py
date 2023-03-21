from django.urls import path
from config import settings
from app_manager.views import ListOfUsersListView
from django.conf.urls.static import static


urlpatterns = [
    path('', ListOfUsersListView.as_view(), name='users_list'),
]