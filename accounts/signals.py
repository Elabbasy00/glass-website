from django.dispatch import receiver
from django.db.models import signals
from .models import User
from allauth.account.signals import user_signed_up, email_confirmed
from .utils import SendSingleSMS, generate_digits

@receiver(signals.post_save, sender=User)
def Send_SMS_After_Creaction(sender, instance, created, **kwargs):
    " send 6 Digits to mobile number"
    if created:
        if instance.phone_number:
            user_phone = instance.phone_number
            number = generate_digits()
            # TODO: Save number to user model
            sms = SendSingleSMS("Your activate code is {}".format(number), user_phone)
        return instance