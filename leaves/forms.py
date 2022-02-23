import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Leave, User


class EmployerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user


class EmployeeSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employer = False
        user.save()
        return user


class LeaveForm(forms.ModelForm):
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


class LeaveDeleteForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = []
