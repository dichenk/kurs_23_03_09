from django.shortcuts import render
from django.views.generic import ListView
from app_users.models import Users



class ListOfUsersListView(ListView):
    model = Users
    template_name = 'app_manager/list_of_users.html'

    def get_queryset(self):
        return User.objects.filter().include(groups__name='manager')