from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

class profile(models.Model):
    name = models.CharField(max_length=128)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    description = models.TextField(default='description default text')

    def __str__(self):
        return self.name

class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username

def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print('Created for %s' %(user.username))
    if user_stripe_account.stripe_id is None or user_stripe_account == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()

def profileCallback(sender, request, user, **kwargs):
    userProfile, is_created = profile.objects.get_or_create(user=user)
    if is_created:
        userProfile = user.username
        userProfile.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(profileCallback)
user_signed_up.connect(stripeCallback)