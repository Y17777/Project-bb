# Generated by Django 5.0.3 on 2024-03-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0003_alter_bullets_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bullets',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
    ]
