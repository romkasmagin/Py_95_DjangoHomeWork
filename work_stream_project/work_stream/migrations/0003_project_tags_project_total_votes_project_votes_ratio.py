# Generated by Django 5.0.3 on 2024-03-10 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_stream', '0002_tag_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='work_stream.tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='total_votes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='votes_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]