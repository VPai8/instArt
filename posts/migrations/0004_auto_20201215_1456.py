# Generated by Django 3.1.3 on 2020-12-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment_last_edit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='last_edit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='last_edit',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
