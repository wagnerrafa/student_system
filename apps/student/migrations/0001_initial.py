# Generated by Django 3.2.16 on 2022-10-08 00:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('create_user', models.UUIDField()),
                ('update_user', models.UUIDField(null=True)),
                ('name', models.CharField(max_length=150, verbose_name='Nome do aluno')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('birthday', models.DateField(verbose_name='Data de aniversário')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
