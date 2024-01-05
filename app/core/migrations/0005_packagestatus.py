# Generated by Django 4.0.10 on 2024-01-03 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_organization_facebook_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(max_length=1)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_update_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_by', models.IntegerField(blank=True, null=True)),
                ('last_update_login', models.IntegerField(null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.organization')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.package')),
            ],
        ),
    ]
