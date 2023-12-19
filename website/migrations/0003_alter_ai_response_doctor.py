# Generated by Django 4.2.5 on 2023-12-19 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_ai_response_userid_ai_response_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai_response',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ai_response_doctor', to=settings.AUTH_USER_MODEL),
        ),
    ]