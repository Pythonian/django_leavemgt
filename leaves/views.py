from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail, mail_admins
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Leave, User
from .forms import (
    EmployerSignUpForm, EmployeeSignUpForm, LeaveForm,
    LeaveDeleteForm)


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
        {'leaves': leaves}
    )


@login_required
def json_records(request):
    leaves = Leave.objects.all()
    data = [leave.get_json() for leave in leaves]
    response = {"data": data}
    return JsonResponse(response)


@login_required
def employee_dashboard(request):
    leaves = Leave.objects.filter(user=request.user)
    # last_leave = Leave.objects.filter(user=request.user).latest()

    return render(
        request, 'employee_dashboard.html',
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
def create_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(
                request, 'Leave Request Sent, Wait For Response')
            from_email = leave.user.email
            to_email = settings.DEFAULT_FROM_EMAIL
            send_mail(
                'A New Leave Application',
                'Check your dashboard for a new Leave application.',
                from_email,
                [to_email])
            return redirect('employee_dashboard')
        else:
            messages.warning(
                request, 'Error! Check form for messages')
    else:
        form = LeaveForm()

    return render(
        request, 'apply_leave_form.html',
        {'form': form})


@login_required
def leave_detail(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    return render(
        request, 'leave_detail.html',
        {'leave': leave})


@login_required
def leave_delete(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        form = LeaveDeleteForm(request.POST, instance=leave)
        if form.is_valid():
            leave.delete()
            messages.success(
                request, "Leave application successfully deleted.")
            return redirect('home')
    else:
        form = LeaveDeleteForm(instance=leave)
    return render(
        request, 'leave_delete_confirm.html',
        {'leave': leave, 'form': form})


@login_required
def leave_approve(request, pk):
    if not request.user.is_employer:
        return redirect('home')
    leave = get_object_or_404(Leave, pk=pk)
    leave.approve_leave
    messages.success(request, f'Leave successfully approved for {leave.user}')
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = leave.user.email
    send_mail(
        'Leave Approved',
        'Your Leave Request Has Now Been Successfully Approved.',
        from_email,
        [to_email])
    return redirect('leave_detail', pk=pk)


def leave_reject(request, pk):
    if not request.user.is_employer:
        return redirect('home')
    leave = get_object_or_404(Leave, pk=pk)
    leave.reject_leave
    messages.success(request, 'Leave request has been rejected')
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = leave.user.email
    send_mail(
        'Leave Rejected',
        'Your Leave Request Has Unfortunately Been Rejected.',
        from_email,
        [to_email])
    return redirect('leave_detail', pk=pk)
