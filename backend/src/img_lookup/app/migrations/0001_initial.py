# Generated by Django 4.2.7 on 2023-12-27 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('file_name', models.TextField()),
                ('file_key', models.TextField()),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection_type', models.TextField(choices=[('text_ocr', 'Text Ocr'), ('google_lens', 'Google Lens')])),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.asset')),
            ],
        ),
    ]
