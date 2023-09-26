from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .manager import CustomUserManager
from django.urls import reverse


USERNAME_REGEX = r'^[\w.@+\- ]+$'



class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, validators=[RegexValidator(
        regex=USERNAME_REGEX, message='الاسم يجب ان يتكون من احرف و ارقام', code='invalid_username')], null=True, blank=True)

    email = models.EmailField(_('email address'), unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
        
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    # phone_number = PhoneNumberField(unique=True, validators=[phone_regex])

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    verification_numbers = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    # class Meta:
    #     verbose_name = 'المستخدمين'
    #     verbose_name_plural = 'المستخدمين'


class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, default=)
    default = models.BooleanField(default=False)


    def get_delete_url(self):
        return reverse("accounts:delete_address", kwargs={
            'id': self.id
        })

    def set_default_url(self):
        return reverse("accounts:default_address", kwargs={
            'id': self.id
        })