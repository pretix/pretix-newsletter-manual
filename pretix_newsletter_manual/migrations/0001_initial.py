# Generated by Django 3.0.14 on 2021-04-17 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pretixbase", "0181_team_can_checkin_orders"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsletterRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pretixbase.Order",
                    ),
                ),
            ],
        ),
    ]
