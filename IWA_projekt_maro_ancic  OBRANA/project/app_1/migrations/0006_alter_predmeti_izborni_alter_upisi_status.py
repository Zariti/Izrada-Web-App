# Generated by Django 4.2.1 on 2023-06-17 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0005_rename_predmet_id_upisi_predmet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmeti',
            name='izborni',
            field=models.CharField(choices=[('da', 'da'), ('ne', 'ne')], max_length=50),
        ),
        migrations.AlterField(
            model_name='upisi',
            name='status',
            field=models.CharField(choices=[('upisan', 'Upisao predmet'), ('polozen', 'Polozio predmet'), ('izg_potpis', 'Izgubio potpis')], max_length=50),
        ),
    ]