from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField, EmailField
from django.db.models import OneToOneField, SET_NULL

from djstripe.models import Subscription
from djstripe import webhooks
import stripe


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
    is_enabled = BooleanField(default=True)


@webhooks.handler("customer.subscription.created")
def customer_subscription_created(event, **kwargs):
    """
    Notify to admins
    """
    print("SUBSCRIPTION CREATED")
    data_object = event.data["object"]
    if data_object["status"] in ["active", "trialing"]:
        subscription = Subscription.objects.get(id=data_object["id"])

        UserSubscription.objects.create(
            stripe_subscription=subscription,
        )
        print("USERSUBSCRIPTION CREATED")


@webhooks.handler("customer.subscription.deleted")
def customer_subscription_deleted(event, **kwargs):
    """
    Workaround for issue: https://github.com/dj-stripe/dj-stripe/issues/855

    When a subscription is finally canceled or 'right now' using the dashboard,
    it is also removed from DB due to a nasty bug

    Re-sync again and mark UserSubscription as disabled

    NOTE: this is not a problem when cancelling a subscription at the end of the period because
    in that case the event triggered is customer.subscription.updated
    """
    print("SUBCRIPTION CANCELLED")
    obj_id = event.data['object']['id']
    stripe_subscription = stripe.Subscription.retrieve(obj_id)
    subscription = Subscription.sync_from_stripe_data(stripe_subscription)
    subscription.lb_sub.is_enabled = False
    subscription.lb_sub.save()
    print("USERSUBSCRIPTION MODIFIED")
