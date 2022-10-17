import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Leave, User, Message


class EmployerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user


class EmployeeSignUpForm(UserCreationForm):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'gender', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'A user with that email already exists.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()
        user.refresh_from_db()
        user.employee.gender = self.cleaned_data.get('gender')
        user.save()
        return user


class LeaveForm(forms.ModelForm):
    ANNUAL = 'annual'
    SICK = 'sick'
    SABBATICAL = 'sabbatical'
    MATERNITY = 'maternity'
    PATERNITY = 'paternity'

    LEAVE_TYPE = (
        (ANNUAL, 'Annual Leave'),
        (SICK, 'Sick Leave'),
        (SABBATICAL, 'Sabbatical Leave'),
        (PATERNITY, 'Paternity Leave'),
        (MATERNITY, 'Maternity Leave'),
    )

    leave_type = forms.ChoiceField(required=True, choices=LEAVE_TYPE)
    reason = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control dateinput',
            'type': 'date',
        }))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control dateinput',
            'type': 'date',
        }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'leave_type', 'reason']

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        today_date = datetime.date.today()

        if (start_date or end_date) < today_date:
            # both dates must not be in the past
            raise forms.ValidationError(
                "Selected dates are incorrect, please select again")
        elif start_date >= end_date:
            # TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
            raise forms.ValidationError("Selected dates are wrong")
        return end_date

    def clean_leave_type(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        dates = (end_date - start_date)
        leave_days = dates.days

        leave_type = self.cleaned_data['leave_type']
        
        if leave_type == Leave.PATERNITY:
            if int(leave_days) > 14:
                raise forms.ValidationError(
                    "Paternity leave shouldn't exceed 14 days. Select new dates above.")

        if leave_type == Leave.SICK:
            if int(leave_days) > 90:
                raise forms.ValidationError(
                    "Sick leave shouldn't exceed 90 days. Select new dates above.")

        # if leave_type == Leave.ANNUAL:
        #     # No employee can apply for anual lave more than once
        #     if Leave.objects.filter(user=self.request.user, leave_type=Leave.ANNUAL).exists():
        #         raise forms.ValidationError('You have already applied for annual leave this year.')
        return leave_type


class LeaveDeleteForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = []


class MessageForm(forms.ModelForm):
    # body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type message here.'}))
    
    class Meta:
        model = Message
        fields = ['body']