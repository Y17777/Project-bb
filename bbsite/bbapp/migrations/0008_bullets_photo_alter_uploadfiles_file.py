# Generated by Django 5.0.3 on 2024-03-12 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0007_uploadfiles_alter_bullets_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bullets',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='uploadfiles',
            name='file',
            field=models.FileField(upload_to='uploads'),
        ),
    ]
