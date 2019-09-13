# Generated by Django 2.2.3 on 2019-09-11 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_playing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Char',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='playing',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='playing',
            name='date',
            field=models.DateField(verbose_name='playing date'),
        ),
    ]