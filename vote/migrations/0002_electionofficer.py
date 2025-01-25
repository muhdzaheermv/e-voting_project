# Generated by Django 4.2.7 on 2025-01-25 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionOfficer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('id_number', models.CharField(max_length=20, unique=True)),
                ('fullname', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('phonenumber', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField()),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
