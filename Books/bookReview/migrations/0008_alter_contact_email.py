# Generated by Django 4.1.6 on 2023-02-08 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookReview', '0007_rename_message_contact_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
