# Generated by Django 2.0.3 on 2018-03-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0002_tab_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tab',
            name='instrument',
            field=models.CharField(choices=[('guitar', 'Guitar'), ('bass', 'Bass'), ('ukelele', 'Ukelele'), ('mixed', 'Mixed'), ('other', 'Other')], default='guitar', max_length=16),
        ),
    ]