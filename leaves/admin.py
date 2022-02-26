from django.contrib import admin

from .models import Leave, User

admin.site.register(User)
admin.site.register(Leave)
