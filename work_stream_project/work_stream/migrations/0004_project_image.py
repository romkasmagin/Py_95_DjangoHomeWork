# Generated by Django 5.0.3 on 2024-03-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_stream', '0003_project_tags_project_total_votes_project_votes_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, default='project_images/default.jpg', null=True, upload_to='project_images'),
        ),
    ]
