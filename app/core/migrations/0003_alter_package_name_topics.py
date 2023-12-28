# Generated by Django 4.0.10 on 2023-12-28 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_organization_package_userrole_user_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('prompt', models.CharField(max_length=255, null=True)),
                ('keywords', models.CharField(max_length=255, null=True)),
                ('platform', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=1, null=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_update_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_by', models.IntegerField(blank=True, null=True)),
                ('last_update_login', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
