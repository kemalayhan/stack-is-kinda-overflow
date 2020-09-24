from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse

from tags.models import Tag



class User(AbstractUser):
    location        = models.CharField(max_length=100, null=True, blank=True)
    biography       = models.TextField(blank=True, null=True)
    image           = models.ImageField(null=True,blank=True, upload_to='users_image')
    github_link     = models.CharField(null=True, blank=True, max_length=100)
    tag             = models.ManyToManyField(Tag, blank=True, null=True)
    created_date    = models.DateField(auto_now_add=True)
    profession      = models.CharField(max_length=100, null=True, blank=True)
    phone           = PhoneNumberField(null=True, blank=True)
    experience      = models.CharField(null=True, blank=True, max_length=100)
    hourly_rate     = models.CharField(default='10$/hr',blank=True, null=True, max_length=30)
    total_project   = models.SmallIntegerField(null=True, blank=True)
    

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"pk": self.pk})
    

