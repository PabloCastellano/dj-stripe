# Generated by Django 3.1.2 on 2020-11-15 18:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import djstripe.fields


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0012_charge_application_fee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plan",
            name="name",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="statement_descriptor",
        ),
        migrations.AddField(
            model_name="plan",
            name="amount_decimal",
            field=djstripe.fields.StripeDecimalCurrencyAmountField(
                blank=True,
                decimal_places=12,
                help_text="The unit amount in cents to be charged, represented as a decimal string with at most 12 decimal places.",
                max_digits=19,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="plan",
            name="active",
            field=models.BooleanField(
                help_text="Whether the plan can be used for new purchases."
            ),
        ),
        migrations.AlterField(
            model_name="plan",
            name="interval_count",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="The number of intervals (specified in the interval property) between each subscription billing.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="plan",
            name="product",
            field=djstripe.fields.StripeForeignKey(
                blank=True,
                help_text="The product whose pricing this plan determines.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="djstripe.product",
                to_field=settings.DJSTRIPE_FOREIGN_KEY_TO_FIELD,
            ),
        ),
        migrations.AlterField(
            model_name="plan",
            name="trial_period_days",
            field=models.IntegerField(
                blank=True,
                help_text="Number of trial period days granted when subscribing a customer to this plan. Null if the plan has no trial period.",
                null=True,
            ),
        ),
    ]