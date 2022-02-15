from django.db import models


class LeaveManager(models.Manager):
    def get_queryset(self):
        '''
        overrides objects.all()
        return all leaves irrespective of status
        '''
        return super().get_queryset()

    def all_pending_leaves(self):
        '''
        gets all pending leaves -> Leave.objects.all_pending_leaves()
        '''
        return super().get_queryset().filter(
            status='P').order_by('-created')

    def all_cancelled_leaves(self):
        '''
        gets all cancelled leaves -> Leave.objects.all_cancelled_leaves()
        '''
        return super().get_queryset().filter(
            status='C').order_by('-created')

    def all_rejected_leaves(self):
        '''
        gets all rejected leaves -> Leave.objects.all_rejected_leaves()
        '''
        return super().get_queryset().filter(
            status='R').order_by('-created')

    def all_approved_leaves(self):
        '''
        gets all approved leaves -> Leave.objects.all_approved_leaves()
        '''
        return super().get_queryset().filter(status='A')
