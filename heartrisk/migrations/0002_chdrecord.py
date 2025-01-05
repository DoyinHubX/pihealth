# Generated by Django 4.2.13 on 2024-12-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("heartrisk", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CHDRecord",
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
                ("male", models.BooleanField(default=False)),
                ("age", models.PositiveIntegerField()),
                ("education", models.PositiveIntegerField()),
                ("current_smoker", models.BooleanField(default=False)),
                ("cigs_per_day", models.PositiveIntegerField(default=0)),
                ("bp_meds", models.BooleanField(default=False)),
                ("prevalent_stroke", models.BooleanField(default=False)),
                ("prevalent_hyp", models.BooleanField(default=False)),
                ("diabetes", models.BooleanField(default=False)),
                ("tot_chol", models.FloatField()),
                ("sys_bp", models.FloatField()),
                ("dia_bp", models.FloatField()),
                ("bmi", models.FloatField()),
                ("heart_rate", models.FloatField()),
                ("glucose", models.FloatField()),
                (
                    "risk_level",
                    models.CharField(
                        choices=[
                            ("At Risk", "At Risk"),
                            ("Not At Risk", "Not At Risk"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
