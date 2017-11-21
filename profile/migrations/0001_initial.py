# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 00:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('personal_id', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(code='nomatch', message='Personal ID has to follow style yyyyMMdd-xxxx', regex='^\\d{8}-\\d{4}$')])),
                ('address', models.CharField(max_length=255)),
                ('address_number', models.CharField(max_length=3)),
                ('post_city', models.CharField(max_length=255)),
                ('post_number', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(code='nomatch', message='Post number has to be 5 long', regex='^\\d{5}$')])),
                ('phone_number', models.CharField(max_length=14)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', profile.models.UserManager()),
            ],
        ),
    ]
