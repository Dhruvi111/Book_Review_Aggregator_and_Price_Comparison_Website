# Generated by Django 4.1.6 on 2023-04-12 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookReview', '0021_remove_userreview_id_userreview_reviewid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreview',
            name='reviewId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]