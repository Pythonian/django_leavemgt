from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(
             redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/employee/',
         views.EmployeeSignUpView.as_view(), name='employee_signup'),
    path('signup/employer/',
         views.EmployerSignUpView.as_view(), name='employer_signup'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('pending-leaves/', views.pending_leaves, name='pending_leaves'),
    path('approved-leaves/', views.approved_leaves, name='approved_leaves'),
    path('rejected-leaves/', views.rejected_leaves, name='rejected_leaves'),
    path('leave/<int:pk>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete'),
    path('leave/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leave/<int:pk>/unapprove/', views.leave_unapprove, name='leave_unapprove'),
    path('leave/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
    path('create-leave/', views.create_leave, name='create_leave'),
    path('', views.home, name='home'),
    # path('leave/apply/', views.leave_creation, name='createleave'),
    # path('leaves/pending/all/', views.leaves_list, name='leaveslist'),
    # path('leaves/approved/all/', views.leaves_approved_list,
    #      name='approvedleaveslist'),
    # path('leaves/cancel/all/', views.cancel_leaves_list, name='canceleaveslist'),
    # path('leaves/all/view/<int:id>/', views.leaves_view, name='userleaveview'),
    # path('leaves/view/table/', views.view_my_leave_table, name='staffleavetable'),
    # path('leave/unapprove/<int:id>/',
    #      views.unapprove_leave, name='userleaveunapprove'),
    # path('leave/cancel/<int:id>/', views.cancel_leave, name='userleavecancel'),
    # path('leave/uncancel/<int:id>/',
    #      views.uncancel_leave, name='userleaveuncancel'),
    # path('leaves/rejected/all/', views.leave_rejected_list, name='leavesrejected'),
    # path('leave/reject/<int:id>/', views.reject_leave, name='reject'),
    # path('leave/unreject/<int:id>/', views.unreject_leave, name='unreject'),
]
