# Generated by Django 4.1.6 on 2023-02-06 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookReview', '0006_contact_subject_alter_contact_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='message',
            new_name='text',
        ),
    ]
