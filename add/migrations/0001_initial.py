# Generated by Django 4.1.2 on 2023-03-08 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Add",
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
                ("name", models.CharField(max_length=70)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("counter", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name="ReportCategory",
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
                ("name", models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name="Saved",
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
                        related_name="add_saved",
                        to="add.add",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_saved",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("add", "owner")},
            },
        ),
        migrations.CreateModel(
            name="Report",
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
                ("cause", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_report",
                        to="add.add",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_report",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "report_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="add.reportcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
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
                ("picture", models.BinaryField(editable=True)),
                (
                    "content_type",
                    models.CharField(
                        help_text="The MIMEType of the file", max_length=256
                    ),
                ),
                ("cover", models.BooleanField(default=False)),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_photo",
                        to="add.add",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OfferedPrice",
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
                ("price_offered", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_offered_price",
                        to="add.add",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_offered_price",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("add", "owner")},
            },
        ),
        migrations.CreateModel(
            name="History",
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
                ("text", models.CharField(max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_history",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
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
        migrations.CreateModel(
            name="Favrioute",
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
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_favrioute",
                        to="add.category",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_favrioute",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("category", "owner")},
            },
        ),
        migrations.CreateModel(
            name="CoverPhoto",
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
                ("picture", models.BinaryField(editable=True)),
                (
                    "content_type",
                    models.CharField(
                        help_text="The MIMEType of the file", max_length=256
                    ),
                ),
                (
                    "add",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cover_photo",
                        to="add.add",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "add",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="add_comment",
                        to="add.add",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_comment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="category",
            name="favrioute",
            field=models.ManyToManyField(
                related_name="user_category_favrioute",
                through="add.Favrioute",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="add.category"
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="comment",
            field=models.ManyToManyField(
                related_name="user_add_comment",
                through="add.Comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="offered_price",
            field=models.ManyToManyField(
                related_name="user_add_offered_price",
                through="add.OfferedPrice",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_add",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="report",
            field=models.ManyToManyField(
                related_name="user_add_report",
                through="add.Report",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="saved",
            field=models.ManyToManyField(
                related_name="user_add_saved",
                through="add.Saved",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="add",
            name="tag",
            field=models.ManyToManyField(blank=True, to="add.tag"),
        ),
    ]
