from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

from .managers import CustomUserManager

def expiry_time():
       return timezone.now() + timezone.timedelta(minutes=15)


class User(AbstractBaseUser, PermissionsMixin):
    phone_no = models.CharField(_('phone_no'), unique=True,max_length=15)
    otp = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_expiry = models.DateTimeField(default = expiry_time(), blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_no

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField( max_length=100)
    address = models.CharField( max_length=255)
    phone_no = models.CharField(max_length=17)
    appointment_date = models.DateTimeField(blank=True)
    photos = models.ImageField(upload_to='images')
    comment = models.TextField()

class SendSMS(models.Model):
    to_number = models.CharField(max_length=30)
    from_number = models.CharField(max_length=30)
    sms_sid = models.CharField(max_length=34, default="", blank=True)
    account_sid = models.CharField(max_length=34, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="", blank=True)