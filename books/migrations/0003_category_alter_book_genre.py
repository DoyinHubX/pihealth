# Generated by Django 4.2.13 on 2024-12-14 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_alter_book_published_date_review"),
    ]

    operations = [
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
                (
                    "name",
                    models.CharField(
                        help_text="Enter the category/genre name",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Enter a brief description of the category",
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="book",
            name="genre",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a book genre",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books",
                to="books.category",
            ),
        ),
    ]
