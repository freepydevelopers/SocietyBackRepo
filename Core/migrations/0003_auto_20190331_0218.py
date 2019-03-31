# Generated by Django 2.1.7 on 2019-03-30 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_auto_20190322_0021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='constructionyear',
            new_name='constructionstatusyear',
        ),
        migrations.AddField(
            model_name='building',
            name='constructionstatus',
            field=models.CharField(choices=[('PRO', 'Proposed'), ('COM', 'Complete'), ('UCO', 'Under Construction'), ('DES', 'Destroyed')], default='COM', max_length=3),
        ),
        migrations.AlterField(
            model_name='flat',
            name='status',
            field=models.CharField(choices=[('empt', 'Empty'), ('iso', 'Is Owner'), ('ist', 'Is Tenant')], default='iso', max_length=3),
        ),
        migrations.AlterField(
            model_name='unitplan',
            name='unittype',
            field=models.CharField(choices=[('01r', '1 Room Kitchen'), ('01b', '1 BHK'), ('15b', '1.5 BHK'), ('02b', '2 BHK'), ('25b', '2.5 BHK'), ('03b', '3 BHK'), ('04b', '4 BHK'), ('pen', 'Penthouse')], default='01b', max_length=3),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='status',
            field=models.CharField(choices=[('adm', 'Admin'), ('own', 'Owner'), ('ten', 'Tenant'), ('emp', 'Employee')], default='own', max_length=3),
        ),
    ]
