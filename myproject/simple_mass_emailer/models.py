
from django.db import models
from django.contrib.auth.models import User


STATE_CHOICES = (
    (""  , "Select..."),
    ("AB", "AB - Alberta"),
    ("AK", "AK - Alaska"),
    ("AL", "AL - Alabama"),
    ("AR", "AR - Arkansas"),
    ("AZ", "AZ - Arizona"),
    ("BC", "BC - British Columbia"),
    ("CA", "CA - California"),
    ("CO", "CO - Colorado"),
    ("CT", "CT - Connecticut"),
    ("DC", "DC - District of Columbia"),
    ("DE", "DE - Deleware"),
    ("FL", "FL - Florida"),
    ("GA", "GA - Georgia"),
    ("HI", "HI - Hawaii"),
    ("IA", "IA - Iowa"),
    ("ID", "ID - Idaho"),
    ("IL", "IL - Illinois"),
    ("IN", "IN - Indiana"),
    ("KS", "KS - Kansas"),
    ("KY", "KY - Kentucky"),
    ("LA", "LA - Louisiana"),
    ("MA", "MA - Massachusetts"),
    ("MB", "MB - Manitoba"),
    ("MD", "MD - Maryland"),
    ("ME", "ME - Maine"),
    ("MI", "MI - Michigan"),
    ("MN", "MN - Minnesota"),
    ("MO", "MO - Missouri"),
    ("MS", "MS - Mississippi"),
    ("MT", "MT - Montana"),
    ("NB", "NB - New Brunswick"),
    ("NC", "NC - North Carolina"),
    ("ND", "ND - North Dakota"),
    ("NE", "NE - Nebraska"),
    ("NF", "NF - Newfoundland"),
    ("NH", "NH - New Hampshire"),
    ("NJ", "NJ - New Jersey"),
    ("NM", "NM - New Mexico"),
    ("NS", "NS - Nova Scotia"),
    ("NT", "NT - North West Territories"),
    ("NV", "NV - Nevada"),
    ("NY", "NY - New York"),
    ("OH", "OH - Ohio"),
    ("OK", "OK - Oklahoma"),
    ("ON", "ON - Ontario"),
    ("OR", "OR - Oregon"),
    ("PA", "PA - Pennsylvania"),
    ("PE", "PE - Prince Edward Island"),
    ("PR", "PR - Puerto Rico"),
    ("QC", "QC - Quebec"),
    ("RI", "RI - Rhode Island"),
    ("SC", "SC - South Carolina"),
    ("SD", "SD - South Dakota"),
    ("SK", "SK - Saskatchewan"),
    ("TN", "TN - Tennessee"),
    ("TX", "TX - Texas"),
    ("UT", "UT - Utah"),
    ("VA", "VA - Virginia"),
    ("VI", "VI - Virgin Islands"),
    ("VT", "VT - Vermont"),
    ("WA", "WA - Washington"),
    ("WI", "WI - Wisconsin"),
    ("WV", "WV - West Virginia"),
    ("WY", "WY - Wyoming"),
    ("YK", "YK - Yukon"),
)


class Agent(models.Model):
    """
    Agent table is used to extend the built-in User table.
    """
    user = models.OneToOneField(User)
    parent = models.ForeignKey(User, related_name='agent_parent', null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=254)
    address2 = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    realtor = models.BooleanField(default=False)
    ins_agent = models.BooleanField(default=False)
    company = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.user.last_name, self.user.first_name)


class Recruit(models.Model):
    """
    Recruit entries are the mass emailer targets.
    """
    sponsor = models.ForeignKey(User)
    email = models.EmailField(db_index=True, max_length=254)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    address1 = models.CharField(max_length=254, null=True, blank=True)
    address2 = models.CharField(max_length=254, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    realtor = models.BooleanField(default=False)
    ins_agent = models.BooleanField(default=False)
    company = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s, %s' % (self.email, self.last_name, self.first_name)


DEFAULT_TARGET_CHOICE = 'NONE'
TARGET_CHOICES = (
    ('AGENT', 'Agent'),
    ('RECRUIT', 'Recruit'),
    ('ALL', 'All'),
    (DEFAULT_TARGET_CHOICE, 'None'),
)


class EmailTemplate(models.Model):
    """
    This table saves the email message templates that will be used to populate
    the EmailMessage table.
    """
    template_code = models.CharField(db_index=True, max_length=50)
    template_name = models.CharField(max_length=254)
    target = models.CharField(max_length=254, choices=TARGET_CHOICES, default=DEFAULT_TARGET_CHOICE)
    message_from = models.CharField(max_length=254, null=True, blank=True, default='')
    message_subject = models.CharField(max_length=254, null=True, blank=True, default='')
    message_text = models.TextField(null=True, blank=True, default='')
    message_html = models.TextField(null=True, blank=True, default='')
    time_created = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s' % (self.template_code, self.template_name)


class EmailMessage(models.Model):
    """
    EmailMessage is non-normalized table that serves as record log for email messages sent.
    """
    email_template = models.ForeignKey(EmailTemplate)
    email = models.EmailField(db_index=True, max_length=254)
    url_key_code = models.CharField(db_index=True, max_length=50)  # using pgsql: md5(random()::text)
    message_from = models.CharField(max_length=254, null=True, blank=True, default='')
    message_subject = models.CharField(max_length=254, null=True, blank=True, default='')
    message_text = models.TextField(null=True, blank=True, default='')
    message_html = models.TextField(null=True, blank=True, default='')
    time_created = models.DateTimeField(auto_now=True, auto_now_add=True)
    send_succeed = models.NullBooleanField(default=False)
    time_email_send = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_form_opened = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_form_submit = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    time_form_cancel = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.email_template.template_code, self.email)
