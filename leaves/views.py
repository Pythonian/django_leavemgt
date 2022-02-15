from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Leave, User, Type
from .forms import EmployerSignUpForm, EmployeeSignUpForm, LeaveForm


@login_required
def home(request):
    if request.user.is_employer:
        return redirect('employer_dashboard')
    else:
        return redirect('employee_dashboard')


class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'an employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('employer_dashboard')


class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'an employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('employee_dashboard')


@login_required
def employer_dashboard(request):
    leaves = Leave.objects.all()

    return render(
        request, 'employer_index.html',
        {'leaves': leaves})


@login_required
def pending_leaves(request):
    leaves = Leave.objects.all_pending_leaves()

    return render(
        request, 'pending_leaves.html',
        {'leaves': leaves})


@login_required
def approved_leaves(request):
    leaves = Leave.objects.all_approved_leaves()

    return render(
        request, 'approved_leaves.html',
        {'leaves': leaves})


@login_required
def rejected_leaves(request):
    leaves = Leave.objects.all_rejected_leaves()

    return render(
        request, 'rejected_leaves.html',
        {'leaves': leaves})


@login_required
def leave_types(request):
    leave_types = Type.objects.all()

    return render(
        request, 'leave_types.html',
        {'leave_types': leave_types})


@login_required
def leave_detail(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    # print(leave.user)
    # employee = Employee.objects.filter(user = leave.user)[0]
    # print(employee)
    return render(
        request, 'dashboard/leave_detail_view.html',
        {'leave': leave, 'employee': employee,
         'title': '{0}-{1} leave'.format(
            leave.user.username,leave.status)})

    return render(
        request, 'leave_detail.html',
        {'leave': leave})


@login_required
def employee_dashboard(request):
    leaves = Leave.objects.filter(user=request.user)
    last_leave = Leave.objects.filter(user=request.user).latest()

    return render(
        request, 'employee_dashboard.html',
        {'leaves': leaves,
         'last_leave': last_leave})


@login_required
def create_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(
                request, 'Leave Request Sent, Wait For Response')
            return redirect('employee_dashboard')
        messages.error(
            request, 'Error! Check form for messages')
        return redirect('employee_dashboard')
    else:
        form = LeaveForm()

    return render(
        request, 'apply_leave_form.html',
        {'form': form})


# def approve_leave(request,id):
#     if not (request.user.is_superuser and request.user.is_authenticated):
#         return redirect('/')
#     leave = get_object_or_404(Leave, id = id)
#     user = leave.user
#     employee = Employee.objects.filter(user = user)[0]
#     leave.approve_leave

#     messages.error(request,'Leave successfully approved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
#     return redirect('dashboard:userleaveview', id = id)


# def cancel_leaves_list(request):
#     if not (request.user.is_superuser and request.user.is_authenticated):
#         return redirect('/')
#     leaves = Leave.objects.all_cancel_leaves()
#     return render(request,'dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})


# def unapprove_leave(request,id):
#     if not (request.user.is_authenticated and request.user.is_superuser):
#         return redirect('/')
#     leave = get_object_or_404(Leave, id = id)
#     leave.unapprove_leave
#     return redirect('dashboard:leaveslist') #redirect to unapproved list


# def cancel_leave(request,id):
#     if not (request.user.is_superuser and request.user.is_authenticated):
#         return redirect('/')
#     leave = get_object_or_404(Leave, id = id)
#     leave.leaves_cancel

#     messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
#     return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# # Current section -> here
# def uncancel_leave(request,id):
#     if not (request.user.is_superuser and request.user.is_authenticated):
#         return redirect('/')
#     leave = get_object_or_404(Leave, id = id)
#     leave.status = 'pending'
#     leave.is_approved = False
#     leave.save()
#     messages.success(
#         request,'Leave is uncanceled,now in pending list')
#     #work on redirecting to instance leave - detail view
#     return redirect('dashboard:canceleaveslist')


# def reject_leave(request,id):
#     dataset = dict()
#     leave = get_object_or_404(Leave, id = id)
#     leave.reject_leave
#     messages.success(request,'Leave is rejected')
#     return redirect('dashboard:leavesrejected')

#     # return HttpResponse(id)


# def unreject_leave(request,id):
#     leave = get_object_or_404(Leave, id = id)
#     leave.status = 'pending'
#     leave.is_approved = False
#     leave.save()
#     messages.success(
#         request, 'Leave is now in pending list')

#     return redirect('dashboard:leavesrejected')



# #  staffs leaves table user only
# def view_my_leave_table(request):
#     # work on the logics
#     if request.user.is_authenticated:
#         user = request.user
#         leaves = Leave.objects.filter(user = user)
#         employee = Employee.objects.filter(user = user).first()
#         print(leaves)
#         dataset = dict()
#         dataset['leave_list'] = leaves
#         dataset['employee'] = employee
#         dataset['title'] = 'Leaves List'
#     else:
#         return redirect('accounts:login')
#     return render(request,'dashboard/staff_leaves_table.html',dataset)
