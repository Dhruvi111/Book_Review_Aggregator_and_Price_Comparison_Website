# Generated by Django 4.1.6 on 2023-03-23 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookReview', '0012_favouritebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favouritebook',
            name='book_id_api',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
