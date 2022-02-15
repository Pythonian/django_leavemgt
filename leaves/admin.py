from django.contrib import admin

from .models import Leave, User, Type

admin.site.register(User)
admin.site.register(Type)
admin.site.register(Leave)
