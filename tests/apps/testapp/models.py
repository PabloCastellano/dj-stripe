from django.db.models.base import Model
from django.db.models.fields import CharField, EmailField
from django.db.models import OneToOneField, SET_NULL

from djstripe.models import Subscription


class Organization(Model):
    """ Model used to test the new custom model setting."""

    email = EmailField()


class StaticEmailOrganization(Model):
    """ Model used to test the new custom model setting."""

    name = CharField(max_length=200, unique=True)

    @property
    def email(self):
        return "static@example.com"


class NoEmailOrganization(Model):
    """ Model used to test the new custom model setting."""

    name = CharField(max_length=200, unique=True)


class UserSubscription(Model):
    """ Model used to test access to reverse relations from webhook handlers."""

    stripe_subscription = OneToOneField(Subscription, null=True, on_delete=SET_NULL, related_name='lb_sub')
