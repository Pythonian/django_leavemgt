# from django.db import models
# from django.conf import settings


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     friends = models.ManyToManyField('Friend', related_name='my_friends')

#     def __str__(self):
#         return self.user


# class Friend(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.profile
        
    