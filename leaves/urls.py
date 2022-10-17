from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(
             redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/employee/',
         views.employee_signup, name='employee_signup'),
    path('signup/employer/',
         views.EmployerSignUpView.as_view(), name='employer_signup'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('chats/', views.inbox, name='inbox'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('send_chat/<int:pk>/', views.send_chat, name='send_chat'),
    path('receive_msg/<int:pk>/', views.received_chat, name='received_chat'),
    path('pending-leaves/', views.pending_leaves, name='pending_leaves'),
    path('approved-leaves/', views.approved_leaves, name='approved_leaves'),
    path('rejected-leaves/', views.rejected_leaves, name='rejected_leaves'),
    path('leave/<int:pk>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete'),
    path('leave/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leave/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
    path('create-leave/', views.create_leave, name='create_leave'),
    path('json/', views.json_records, name='json_records'),
    path('', views.home, name='home'),
]
