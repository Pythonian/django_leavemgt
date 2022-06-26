from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


# prevent back button in broswer (after logout)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def inbox(request):

    return render(request, 'inbox.html')
