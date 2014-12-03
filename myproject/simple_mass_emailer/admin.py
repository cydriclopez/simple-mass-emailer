
from __future__ import print_function
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import connection
from django.utils.html import strip_tags
from django.core.mail import send_mail, send_mass_mail
from .models import Agent, Recruit, EmailTemplate, EmailMessage
from datetime import datetime
import sys

def print_info(*objs):
    print("INFO: ", *objs, file=sys.stderr)


################################################################################
#
# This is where the action of creating then sending the emails happen.
#
class MassEmailer(object):

    def __init__(self, queryset):
        self.queryset = queryset

    @staticmethod
    def email_sent_timestamp(emailmessage_id):
        # Keep record of when the email was sent.
        EmailMessage.objects.filter(id=emailmessage_id).update(
            send_succeed = True,
            time_email_send = datetime.now()
        )

    @staticmethod
    def form_open_timestamp(emailmessage_id):
        # Keep record of when the form was opened.
        EmailMessage.objects.filter(id=emailmessage_id).update(
            time_form_opened = datetime.now()
        )

    @staticmethod
    def form_submit_timestamp(emailmessage_id):
        # Keep record of when the form was submitted.
        EmailMessage.objects.filter(id=emailmessage_id).update(
            time_form_submit = datetime.now()
        )

    @staticmethod
    def form_cancel_timestamp(emailmessage_id):
        # Keep record of when the form was cancelled.
        EmailMessage.objects.filter(id=emailmessage_id).update(
            time_form_cancel = datetime.now()
        )

    def create_email(self):
        """
        Call PostgreSQL stored function to create email messages.
        """
        cursor = connection.cursor()
        for template in self.queryset:
            print_info('template.template_code:')
            print_info(template.template_code)
            cursor.execute('SELECT create_message(%s)', [template.template_code])

    def send_email(self):
        """
        Loop through EmailMessage and send email messages.
        """
        for template in self.queryset:
            massEmail = EmailMessage.objects.filter(email_template=template)
            for e in massEmail:
                message_sent = False

                try:
                    send_mail(
                        subject = e.message_subject,
                        message = e.message_text,
                        from_email = e.message_from,
                        recipient_list = [e.email],
                        fail_silently = False,
                        html_message = e.message_html
                    )
                    message_sent = True

                except:
                    print_info('failed send email')

                # Keep record of when the email was sent.
                if message_sent:
                    MassEmailer.email_sent_timestamp(e.id)

################################################################################


# Define an inline admin descriptor for Agent model
# which acts a bit like a singleton
class AgentInline(admin.StackedInline):
    model = Agent
    can_delete = False
    verbose_name_plural = 'agent'
    fk_name = 'user'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (AgentInline, )


def send_email(modeladmin, request, queryset):
    mass_emailer = MassEmailer(queryset)
    mass_emailer.create_email()
    mass_emailer.send_email()

send_email.short_description = "Send email using chosen template"


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_code', 'template_name', 'target', 'time_created']
    ordering = ['template_code']
    actions = [send_email]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Exclude Agent because it is now 'stacked inline' with User
# admin.site.register(Agent)
admin.site.register(Recruit)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(EmailMessage)
