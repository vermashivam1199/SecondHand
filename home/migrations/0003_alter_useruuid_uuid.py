# Generated by Django 4.1.2 on 2023-02-15 16:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_remove_useruuid_id_alter_useruuid_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useruuid",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
