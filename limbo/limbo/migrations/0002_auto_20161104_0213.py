# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 02:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('limbo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instr_Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstrType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('service_email', models.CharField(max_length=50, null=True)),
                ('servie_website', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=50, unique=True)),
                ('asset_number', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('FK_instr_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='limbo.InstrType')),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('descriton', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UsageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('FK_instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='limbo.Instrument')),
            ],
        ),
        migrations.CreateModel(
            name='User_Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(max_length=50)),
                ('cmd_line_script', models.CharField(max_length=250)),
                ('SOP', models.TextField()),
                ('FK_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limbo.Method')),
            ],
        ),
        migrations.AddField(
            model_name='user_version',
            name='FK_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limbo.UserProfile'),
        ),
        migrations.AddField(
            model_name='user_version',
            name='FK_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limbo.Version'),
        ),
        migrations.AddField(
            model_name='user_version',
            name='authorizing_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='limbo.UserProfile'),
        ),
        migrations.AddField(
            model_name='usagehistory',
            name='FK_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='limbo.UserProfile'),
        ),
        migrations.AddField(
            model_name='usagehistory',
            name='FK_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='limbo.Version'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='Instr_Version',
            field=models.ManyToManyField(related_name='Instr_Version', through='limbo.Instr_Version', to='limbo.Version'),
        ),
        migrations.AddField(
            model_name='instr_version',
            name='FK_instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limbo.Instrument'),
        ),
        migrations.AddField(
            model_name='instr_version',
            name='FK_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limbo.Version'),
        ),
        migrations.AddField(
            model_name='instr_version',
            name='validating_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='limbo.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('version_number', 'FK_method')]),
        ),
        migrations.AlterUniqueTogether(
            name='user_version',
            unique_together=set([('FK_version', 'FK_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='instr_version',
            unique_together=set([('FK_version', 'FK_instrument')]),
        ),
    ]