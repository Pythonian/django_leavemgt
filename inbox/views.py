from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# from .models import Friend
# from .forms import MessageForm

# prevent back button in broswer (after logout)
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required
# def inbox(request):
#     # user = request.user.profile
#     # List out all the Employees
#     # friends = user.friends.all()
#     context = {
#         # 'user': user, 
#         # 'friends': friends
#     }
#     return render(request, 'inbox.html', context)


def friend(request, pk):
    # Access the chat page for each employee
    friend = get_object_or_404(Friend, pk=pk)
    context = {
        'friend': friend,
        # 'form': MessageForm()
    }
    return render(request, 'friend.html', context)
