from django.contrib import admin

from .models import Leave, User, Employee, Employer, Message

admin.site.register([User, Leave, Employee, Employer, Message])
