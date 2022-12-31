import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.db import transaction
from django.core.mail import send_mail, mail_admins
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Leave, Message, User, Employee, Employer
from .forms import (
    EmployerSignUpForm, EmployeeSignUpForm, LeaveForm,
    LeaveDeleteForm, MessageForm)


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


@transaction.atomic
def employee_signup(request):
    if request.method == "POST":
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Signup successful.")
            return redirect('employee_dashboard')
        else:
            messages.warning(
                request, "An error occured. Please check below.")
    else:
        form = EmployeeSignUpForm()

    template_name = "registration/signup.html"
    context = {
        "form": form,
        "user_type": "an employee",
    }

    return render(request, template_name, context)


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
    last_leave = Leave.objects.filter(user=request.user).latest()
    remaining = ''
    if last_leave.start_date == datetime.datetime.now().date():
        remaining = (last_leave.end_date - datetime.datetime.now().date()).days
        if remaining < 5:
            to_email = request.user.email
            send_mail(
                'Leave Deadline Notification',
                f'This is to notify you that you have less than 5 days to the end of your leave.', 'webmaster@localhost', [to_email])
    
    return render(
        request, 'employee_dashboard.html',
        {'leaves': leaves, 'remaining': remaining})


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
        form = LeaveForm(request.POST, request=request)
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
        form = LeaveForm(request=request)

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


@login_required
def inbox(request):
    if request.user.is_employer:
        contacts = User.objects.filter(is_employee=True)
        messages = Message.objects.all()
    else:
        contacts = User.objects.filter(is_employer=True)
    
    context = {
        'contacts': contacts,
    }
    return render(request, 'inbox.html', context)


@login_required
def chat(request, pk):
    if request.user.is_employer:
        contacts = User.objects.filter(is_employee=True)
    else:
        contacts = User.objects.filter(is_employer=True)
    contact = get_object_or_404(User, pk=pk)
    chats = Message.objects.all()
    rec_chats = Message.objects.filter(sender=contact, receiver=request.user)
    # chats = Message.objects.filter(sender=contact, receiver=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = contact
            chat.save()
            return redirect('chat', pk=contact.pk)
    else:
        form = MessageForm()
    context = {
        'contacts': contacts,
        'contact': contact,
        'form': form,
        'chats': chats,
        'num': rec_chats.count(),
    }
    return render(request, 'chat.html', context)


def send_chat(request, pk):
    data = json.loads(request.body)
    receiver = get_object_or_404(User, pk=pk)
    new_chat = data['body']
    new_chat_message = Message.objects.create(
        body=new_chat, sender=request.user, receiver=receiver, seen=False)
    return JsonResponse(new_chat_message.body, safe=False)


def received_chat(request, pk):
    receiver = get_object_or_404(User, pk=pk)
    array_chats = []
    chats = Message.objects.filter(sender=receiver, receiver=request.user)
    for chat in chats:
        array_chats.append(chat.body)
    return JsonResponse(array_chats, safe=False)