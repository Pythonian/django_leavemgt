import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import LeaveManager


class User(AbstractUser):
    is_employer = models.BooleanField(default=True)


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='employer_profile')

    def __str__(self):
        return f"Profile for {self.user.username}"


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='employee_profile')

    def __str__(self):
        return f"Profile for {self.user.username}"


class Type(models.Model):
    name = models.CharField('Leave Type', max_length=15)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Leave(models.Model):
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    CANCELLED = 'C'
    LEAVE_STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    )

    SICK = 'sick'
    CASUAL = 'casual'
    EMERGENCY = 'emergency'
    STUDY = 'study'
    MATERNITY = 'maternity'
    PATERNITY = 'paternity'

    LEAVE_TYPE = (
        (SICK, 'Sick Leave'),
        (CASUAL, 'Casual Leave'),
        (EMERGENCY, 'Emergency Leave'),
        (STUDY, 'Study Leave'),
        (PATERNITY, 'Paternity Leave'),
        (MATERNITY, 'Maternity Leave'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField(
        help_text='Leave starts on...')
    end_date = models.DateField(
        help_text='Leave ends on...')
    leave_type = models.CharField(
        max_length=50, choices=LEAVE_TYPE)
    reason = models.CharField(
        'Reason for Leave', max_length=255)
    status = models.CharField(
        max_length=1, choices=LEAVE_STATUS, default=PENDING)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = LeaveManager()

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'

    def __str__(self):
        return f'{self.leave_type} - {self.user} - {self.status}'

    @property
    def leave_days(self):
        start_date = self.start_date
        end_date = self.end_date
        if start_date > end_date:
            return
        dates = (end_date - start_date)
        return dates.days

    @property
    def remaining_days(self):
        # remaining = None
        # if self.is_approved:
        remaining = (
            datetime.datetime.now().date() - self.end_date).days
        return str(remaining)

    # @property
    # def leave_approved(self):
    #     return self.is_approved == True

    # @property
    # def approve_leave(self):
    #     if not self.is_approved:
    #         self.is_approved = True
    #         self.status = 'approved'
    #         self.save()

    # @property
    # def unapprove_leave(self):
    #     if self.is_approved:
    #         self.is_approved = False
    #         self.status = 'pending'
    #         self.save()

    # @property
    # def leaves_cancel(self):
    #     if self.is_approved or not self.is_approved:
    #         self.is_approved = False
    #         self.status = 'cancelled'
    #         self.save()

    # @property
    # def reject_leave(self):
    #     if self.is_approved or not self.is_approved:
    #         self.is_approved = False
    #         self.status = 'rejected'
    #         self.save()

    # @property
    # def is_rejected(self):
    #     return self.status == 'rejected'
