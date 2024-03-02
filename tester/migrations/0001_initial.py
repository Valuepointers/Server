# Generated by Django 4.2.9 on 2024-03-02 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("country", models.CharField(max_length=100)),
                ("founded", models.CharField(max_length=100)),
                ("ipo_date", models.CharField(max_length=100)),
                ("industry", models.CharField(max_length=100)),
                ("sector", models.CharField(max_length=100)),
                ("employees", models.CharField(max_length=100)),
                ("ceo", models.CharField(max_length=100)),
                ("ticker_symbol", models.CharField(max_length=100)),
                ("exchange", models.CharField(max_length=100)),
                ("fiscal_year", models.CharField(max_length=100)),
                ("reporting_currency", models.CharField(max_length=100)),
                ("cik_code", models.CharField(max_length=100)),
                ("cusip_number", models.CharField(max_length=100)),
                ("isin_number", models.CharField(max_length=100)),
                ("employer_id", models.CharField(max_length=100)),
                ("sic_code", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "kakao_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
