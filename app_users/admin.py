from django.contrib import admin

from app_users.models import Users

admin.site.register(Users)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)