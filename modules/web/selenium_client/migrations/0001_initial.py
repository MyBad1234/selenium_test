# Generated by Django 4.2.2 on 2023-06-13 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('word', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=50)),
            ],
        ),
    ]