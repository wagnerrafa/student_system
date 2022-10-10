# Generated by Django 3.2.16 on 2022-10-10 03:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('create_user', models.UUIDField()),
                ('update_user', models.UUIDField(null=True)),
                ('name', models.CharField(max_length=150, verbose_name='Nome da disciplina')),
                ('workload', models.PositiveIntegerField(verbose_name='Carga horária')),
            ],
            options={
                'verbose_name': 'Disciplina',
            },
        ),
    ]
