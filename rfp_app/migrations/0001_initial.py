# Generated by Django 4.2.1 on 2023-06-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RFP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_date', models.CharField(default='N/A', max_length=100)),
                ('due_date', models.CharField(default='N/A', max_length=100)),
                ('rfx_bid_number', models.CharField(default='N/A', max_length=100)),
                ('rfx_type', models.CharField(default='N/A', max_length=100)),
                ('title', models.CharField(default='N/A', max_length=100)),
                ('description', models.CharField(default='N/A', max_length=100)),
                ('buyer_agent_name', models.CharField(default='N/A', max_length=100)),
                ('buyer_agent_email', models.CharField(default='N/A', max_length=100)),
                ('buyer_agent_title', models.CharField(default='N/A', max_length=100)),
                ('sent_to_ms_teams', models.BooleanField(default=False)),
            ],
        ),
    ]
