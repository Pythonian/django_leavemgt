# Generated by Django 4.0.2 on 2022-05-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=10),
            preserve_default=False,
        ),
    ]
