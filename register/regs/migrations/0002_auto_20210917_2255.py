# Generated by Django 3.2.7 on 2021-09-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reg',
            name='course_semester',
            field=models.CharField(choices=[('1', '1'), ('2', '2')], max_length=200),
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]