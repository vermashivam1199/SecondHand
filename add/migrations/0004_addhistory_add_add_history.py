# Generated by Django 4.1.2 on 2023-04-09 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("add", "0003_remove_add_add_history"),
    ]

    operations = [
        migrations.CreateModel(
            name="AddHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_history_thru",
                        to="add.add",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_history_thru",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="add",
            name="add_history",
            field=models.ManyToManyField(
                related_name="user_add_history",
                through="add.AddHistory",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
