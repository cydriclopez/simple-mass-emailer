# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=100, null=True, blank=True)),
                ('address1', models.CharField(max_length=254)),
                ('address2', models.CharField(max_length=254, null=True, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=100, null=True, choices=[(b'', b'Select...'), (b'AB', b'AB - Alberta'), (b'AK', b'AK - Alaska'), (b'AL', b'AL - Alabama'), (b'AR', b'AR - Arkansas'), (b'AZ', b'AZ - Arizona'), (b'BC', b'BC - British Columbia'), (b'CA', b'CA - California'), (b'CO', b'CO - Colorado'), (b'CT', b'CT - Connecticut'), (b'DC', b'DC - District of Columbia'), (b'DE', b'DE - Deleware'), (b'FL', b'FL - Florida'), (b'GA', b'GA - Georgia'), (b'HI', b'HI - Hawaii'), (b'IA', b'IA - Iowa'), (b'ID', b'ID - Idaho'), (b'IL', b'IL - Illinois'), (b'IN', b'IN - Indiana'), (b'KS', b'KS - Kansas'), (b'KY', b'KY - Kentucky'), (b'LA', b'LA - Louisiana'), (b'MA', b'MA - Massachusetts'), (b'MB', b'MB - Manitoba'), (b'MD', b'MD - Maryland'), (b'ME', b'ME - Maine'), (b'MI', b'MI - Michigan'), (b'MN', b'MN - Minnesota'), (b'MO', b'MO - Missouri'), (b'MS', b'MS - Mississippi'), (b'MT', b'MT - Montana'), (b'NB', b'NB - New Brunswick'), (b'NC', b'NC - North Carolina'), (b'ND', b'ND - North Dakota'), (b'NE', b'NE - Nebraska'), (b'NF', b'NF - Newfoundland'), (b'NH', b'NH - New Hampshire'), (b'NJ', b'NJ - New Jersey'), (b'NM', b'NM - New Mexico'), (b'NS', b'NS - Nova Scotia'), (b'NT', b'NT - North West Territories'), (b'NV', b'NV - Nevada'), (b'NY', b'NY - New York'), (b'OH', b'OH - Ohio'), (b'OK', b'OK - Oklahoma'), (b'ON', b'ON - Ontario'), (b'OR', b'OR - Oregon'), (b'PA', b'PA - Pennsylvania'), (b'PE', b'PE - Prince Edward Island'), (b'PR', b'PR - Puerto Rico'), (b'QC', b'QC - Quebec'), (b'RI', b'RI - Rhode Island'), (b'SC', b'SC - South Carolina'), (b'SD', b'SD - South Dakota'), (b'SK', b'SK - Saskatchewan'), (b'TN', b'TN - Tennessee'), (b'TX', b'TX - Texas'), (b'UT', b'UT - Utah'), (b'VA', b'VA - Virginia'), (b'VI', b'VI - Virgin Islands'), (b'VT', b'VT - Vermont'), (b'WA', b'WA - Washington'), (b'WI', b'WI - Wisconsin'), (b'WV', b'WV - West Virginia'), (b'WY', b'WY - Wyoming'), (b'YK', b'YK - Yukon')])),
                ('zipcode', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=100)),
                ('realtor', models.BooleanField(default=False)),
                ('ins_agent', models.BooleanField(default=False)),
                ('company', models.CharField(max_length=100, null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='agent_parent', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('url_key_code', models.CharField(max_length=50, db_index=True)),
                ('message_from', models.CharField(default=b'', max_length=254, null=True, blank=True)),
                ('message_subject', models.CharField(default=b'', max_length=254, null=True, blank=True)),
                ('message_text', models.TextField(default=b'', null=True, blank=True)),
                ('message_html', models.TextField(default=b'', null=True, blank=True)),
                ('time_created', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('send_succeed', models.NullBooleanField(default=False)),
                ('time_email_send', models.DateTimeField(null=True, blank=True)),
                ('time_form_opened', models.DateTimeField(null=True, blank=True)),
                ('time_form_submit', models.DateTimeField(null=True, blank=True)),
                ('time_form_cancel', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template_code', models.CharField(max_length=50, db_index=True)),
                ('template_name', models.CharField(max_length=254)),
                ('target', models.CharField(default=b'NONE', max_length=254, choices=[(b'AGENT', b'Agent'), (b'RECRUIT', b'Recruit'), (b'ALL', b'All'), (b'NONE', b'None')])),
                ('message_from', models.CharField(default=b'', max_length=254, null=True, blank=True)),
                ('message_subject', models.CharField(default=b'', max_length=254, null=True, blank=True)),
                ('message_text', models.TextField(default=b'', null=True, blank=True)),
                ('message_html', models.TextField(default=b'', null=True, blank=True)),
                ('time_created', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('first_name', models.CharField(max_length=254, null=True, blank=True)),
                ('last_name', models.CharField(max_length=254, null=True, blank=True)),
                ('address1', models.CharField(max_length=254, null=True, blank=True)),
                ('address2', models.CharField(max_length=254, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True, choices=[(b'', b'Select...'), (b'AB', b'AB - Alberta'), (b'AK', b'AK - Alaska'), (b'AL', b'AL - Alabama'), (b'AR', b'AR - Arkansas'), (b'AZ', b'AZ - Arizona'), (b'BC', b'BC - British Columbia'), (b'CA', b'CA - California'), (b'CO', b'CO - Colorado'), (b'CT', b'CT - Connecticut'), (b'DC', b'DC - District of Columbia'), (b'DE', b'DE - Deleware'), (b'FL', b'FL - Florida'), (b'GA', b'GA - Georgia'), (b'HI', b'HI - Hawaii'), (b'IA', b'IA - Iowa'), (b'ID', b'ID - Idaho'), (b'IL', b'IL - Illinois'), (b'IN', b'IN - Indiana'), (b'KS', b'KS - Kansas'), (b'KY', b'KY - Kentucky'), (b'LA', b'LA - Louisiana'), (b'MA', b'MA - Massachusetts'), (b'MB', b'MB - Manitoba'), (b'MD', b'MD - Maryland'), (b'ME', b'ME - Maine'), (b'MI', b'MI - Michigan'), (b'MN', b'MN - Minnesota'), (b'MO', b'MO - Missouri'), (b'MS', b'MS - Mississippi'), (b'MT', b'MT - Montana'), (b'NB', b'NB - New Brunswick'), (b'NC', b'NC - North Carolina'), (b'ND', b'ND - North Dakota'), (b'NE', b'NE - Nebraska'), (b'NF', b'NF - Newfoundland'), (b'NH', b'NH - New Hampshire'), (b'NJ', b'NJ - New Jersey'), (b'NM', b'NM - New Mexico'), (b'NS', b'NS - Nova Scotia'), (b'NT', b'NT - North West Territories'), (b'NV', b'NV - Nevada'), (b'NY', b'NY - New York'), (b'OH', b'OH - Ohio'), (b'OK', b'OK - Oklahoma'), (b'ON', b'ON - Ontario'), (b'OR', b'OR - Oregon'), (b'PA', b'PA - Pennsylvania'), (b'PE', b'PE - Prince Edward Island'), (b'PR', b'PR - Puerto Rico'), (b'QC', b'QC - Quebec'), (b'RI', b'RI - Rhode Island'), (b'SC', b'SC - South Carolina'), (b'SD', b'SD - South Dakota'), (b'SK', b'SK - Saskatchewan'), (b'TN', b'TN - Tennessee'), (b'TX', b'TX - Texas'), (b'UT', b'UT - Utah'), (b'VA', b'VA - Virginia'), (b'VI', b'VI - Virgin Islands'), (b'VT', b'VT - Vermont'), (b'WA', b'WA - Washington'), (b'WI', b'WI - Wisconsin'), (b'WV', b'WV - West Virginia'), (b'WY', b'WY - Wyoming'), (b'YK', b'YK - Yukon')])),
                ('zipcode', models.CharField(max_length=50, null=True, blank=True)),
                ('phone', models.CharField(max_length=100, null=True, blank=True)),
                ('realtor', models.BooleanField(default=False)),
                ('ins_agent', models.BooleanField(default=False)),
                ('company', models.CharField(max_length=100, null=True, blank=True)),
                ('sponsor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='email_template',
            field=models.ForeignKey(to='simple_mass_emailer.EmailTemplate'),
            preserve_default=True,
        ),
    ]
