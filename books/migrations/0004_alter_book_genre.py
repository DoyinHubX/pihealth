# Generated by Django 4.2.13 on 2024-12-14 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_category_alter_book_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="genre",
            field=models.ForeignKey(
                blank=True,
                help_text="Select the book genre",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="books.category",
            ),
        ),
    ]
