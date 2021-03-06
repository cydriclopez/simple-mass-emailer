simple-mass-emailer
===================

A simple mass emailer in Django + PostgreSQL.

This version is good for generating hundreds of emails.
To reliably send thousands of mass email the next version will
include the use of Celery + RabbitMQ.

The class `simple_mass_emailer.admin.MassEmailer() <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/admin.py#L21>`_
is demo for a quick easy way to create a custom action in Django's admin interface.

The Django Class-Based-View (CBV) `simple_mass_emailer.views.EnrollFormView() <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/views.py#L18>`_
is a demo for a quick easy mobile-friendly (using `Bootstrap <http://getbootstrap.com/>`_) data entry form
(`enrollment_form.html <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/template/enrollment_form.html>`_)
for a simple application.

Admin-based interface
---------------------

**Click "Email templates" to create email templates.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_click_email_templates.png


**Create/Edit an email template.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_create_edit_email_template.png


**Create a recruit/target email initial entry. In the sent email a link to a form is used to fill-in more info.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_add_recruit_email.png


**List of Email templates.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_list_email_template.png


**Choose a template and "Send email using chosen template" from pull-down menu.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_choose_send_email_using_template.png


Includes a sample form "Affiliate Signup Form"
----------------------------------------------

**This is a sample email sent to target email. Clicking on the link opens a mobile-friendly form.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_affiliate_email.png


**Mobile-friendly form (using Bootstrap) used to fill-in the rest of recruit/target information.**

.. image:: /myproject/simple_mass_emailer/static/img/demo_affiliate_signup_form.png

PostgreSQL
----------
This project uses the PostgreSQL database. The plpgsql stored function
`create_message.sql <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/sql/create_message.sql>`_
creates the email message using the template chosen in EmailTemplate and stuff them into table EmailMessage.
This EmailMessage table is a non-normalized table that serves as record log for email messages sent.

Testing
-------
Note that the classmethod `simple_mass_emailer.tests.Test_main.setUpClass() <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/tests.py#L25>`_
loads the file `create_message.sql <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/sql/create_message.sql>`_.

For testing (`tests.py <https://github.com/cydriclopez/simple-mass-emailer/blob/master/myproject/simple_mass_emailer/tests.py>`_)
to work make sure the login/password account into PostgreSQL has the role right to create a database:
::
    postgres=# ALTER USER username CREATEDB;
