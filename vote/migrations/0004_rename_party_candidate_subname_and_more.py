# Generated by Django 4.2.7 on 2025-01-25 21:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_voter_candidate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='party',
            new_name='subname',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='votes_received',
        ),
        migrations.AddField(
            model_name='candidate',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='candidates/'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='vote.election'),
        ),
        migrations.DeleteModel(
            name='Voter',
        ),
    ]
