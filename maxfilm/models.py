from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Class UserProfile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    birth_date = models.DateField(blank=False, null=False)
    photo = models.ImageField(upload_to='profiles', blank=False, null=False)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username
