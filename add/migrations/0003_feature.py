# Generated by Django 4.1.2 on 2022-11-10 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("add", "0002_favrioute_category_favrioute"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feature",
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
                ("feature_name", models.CharField(max_length=256)),
                ("feature", models.CharField(max_length=256)),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_feature",
                        to="add.add",
                    ),
                ),
            ],
        ),
    ]
