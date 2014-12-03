
from datetime import datetime, date
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.db import models, connection
from django.utils.text import slugify
from myproject import settings
from .models import Agent, Recruit, EmailTemplate, EmailMessage
from .forms import RecruitModelForm
from .admin import MassEmailer
import os
import hashlib


class Test_main(TestCase):
    # Test User entry
    username = 'dmitry_baevsky'
    first_name = 'Dmitry'
    last_name = 'Baevsky'
    email = 'dmitry_baevsky@geemail.com'
    password = 'bestaltoistnow'

    @classmethod
    def setUpClass(cls):
        """
        Create plpgsql stored procedures in the test database
        The file all.sql is the compilation of all stored procedures used.
        It is created by the following:

        cd into folder myproject/badmeter and then run:
        cat sql/* > all.sql
        """
        f = open('/home/user1/Projects/simple-mass-emailer/simple-mass-emailer/myproject/simple_mass_emailer/sql/create_message.sql')
        sql = f.read()
        f.close()
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.connection.commit()

        # Set EMAIL_BACKEND to dummy so no action is done on sending email.
        settings.EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    def add_user_test(self):
        user = User.objects.create_user(
            username = self.username,
            first_name = self.first_name,
            last_name = self.last_name,
            email = self.email,
            password = self.password
        )
        user.save()

    def add_agent_test(self):
        user = User.objects.get(username=self.username)

        agent = Agent.objects.create(
            user = user,
            address1 = '1010 Righthere Ln',
            city = 'New York',
            zipcode = '10077',
            phone = '8881234567',
            realtor = True
        )
        agent.save()

    def add_recruit_email_test(self):
        sponsor = User.objects.get(username=self.username)

        recruit = Recruit.objects.create(
            sponsor = sponsor,
            email = 'johnny_recruit@geemail.com'
        )
        recruit.save()

    def add_email_template_test(self):
        email_template = EmailTemplate.objects.create(
            template_code = 'mars_vacation',
            template_name = 'Vacation to Mars',
            target = 'Recruit',
            message_from = 'noreply@nasainc.com',
            message_subject = 'Vacation to Mars',
            message_text = ''
                'Nasa Inc.\n\n'
                'Hello:\n\n'
                'Do you want to go on vacation to Mars? We have just'
                'the perfect vacation for you! We offer a one-way'
                'trip to Mars where you can meet them friendly Martians.'
                'If you are interested just click on the link below.\n\n'
                'Yes I want to go on vacation to Mars!\n'
                'localhost:8000/enroll-email/##_MD5RANDOM_##/\n\n'
                'Thanks, have a lovely day.\n'
                '##_SPONSOR_##',
            message_html = ''
                '<h1 style="color:red">Nasa Inc.</h1>'
                '<h3>Hello:</h3>'
                '<p>Do you want to go on vacation to Mars? We have just'
                'the perfect vacation for you! We offer a one-way'
                'trip to Mars where you can meet them friendly Martians.'
                'If you are interested just click on the link below.</p>'
                '<p><a href="localhost:8000/enroll-email/##_MD5RANDOM_##/">'
                'Yes I want to go on vacation to Mars!</a></p>'
                '<p>Thanks, have a lovely day.</p>'
                '<p>##_SPONSOR_##</p>',
            time_created = datetime.now()
        )
        email_template.save()

    def test_main(self):
        """
        This is the main test function.
        """
        email = 'johnny_recruit@geemail.com'
        first_name = 'Johnny'
        last_name = 'Recruit'
        address1 = '100 Lost Ln #1'
        city = 'San Francisco'
        state = 'CA'
        zipcode = '94577'
        phone = '4151234567'
        realtor = True
        ins_agent = False

        # Create a user.
        self.add_user_test()
        user = User.objects.filter(username=self.username)
        self.assertTrue(user)

        # Add an agent and link it to a user record.
        self.add_agent_test()
        agent = Agent.objects.filter(user__username=self.username)
        self.assertTrue(agent)

        # Create target recruit record.
        self.add_recruit_email_test()
        recruit = Recruit.objects.filter(email=email)
        self.assertTrue(recruit)

        # Create email template.
        self.add_email_template_test()
        email_template = EmailTemplate.objects.filter(template_code='mars_vacation')
        self.assertTrue(email_template)

        # Create mass email messages then send them.
        mass_emailer = MassEmailer(email_template)
        mass_emailer.create_email()
        mass_emailer.send_email()

        # Check if mass email messages were created and stuffed into table EmailMessage.
        email_message = EmailMessage.objects.filter(email_template__template_code = 'mars_vacation')
        self.assertTrue(email_message)

        # Test using Django view.
        client = Client()
        url_key_code = email_message[0].url_key_code
        url = '/enroll-email/%s/' % url_key_code

        response = client.get(url)
        self.assertContains(response, email, status_code=200)

        # Submit a POST entry into the url.
        response = client.post(url, {
            'first_name' : first_name,
            'last_name' : last_name,
            'address1' : address1,
            'city' : city,
            'state' : state,
            'zipcode' : zipcode,
            'phone' : phone,
            'realtor' : realtor,
            'ins_agent' : ins_agent
        })
        self.assertEqual(response.status_code, 302)

        # Try GET the url and see if initial entries are the same
        # as entries in the immediate previous POST entries.
        response = client.get(url)
        self.assertContains(response, email, status_code=200)
        self.assertContains(response, last_name, status_code=200)
        self.assertContains(response, address1, status_code=200)
        self.assertContains(response, city, status_code=200)
        self.assertContains(response, state, status_code=200)
        self.assertContains(response, zipcode, status_code=200)
        self.assertContains(response, phone, status_code=200)
        self.assertContains(response, 'checked', status_code=200)

        # Simulate error in url by feeding it a random key.
        url = '/enroll-email/%s/' % hashlib.md5(os.urandom(5)).hexdigest()
        response = client.get(url)
        self.assertContains(response, 'Error: Cannot find', status_code=200)

        # Simulate success in posting entries.
        url = '/enroll-success/%s/' % url_key_code
        response = client.get(url)
        self.assertContains(response, 'Thank you', status_code=200)

        # Simulate cancelling entries.
        url = '/enroll-cancel/%s/' % url_key_code
        response = client.get(url)
        self.assertContains(response, 'sign up soon.', status_code=200)
