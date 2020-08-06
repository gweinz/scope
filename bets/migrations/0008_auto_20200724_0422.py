# Generated by Django 3.0.7 on 2020-07-24 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0007_bet_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='is_entered',
            field=models.BooleanField(default=False),
        ),
    ]