
from __future__ import print_function
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from .models import Recruit, EmailMessage, STATE_CHOICES
from .forms import RecruitModelForm
from .admin import MassEmailer
from datetime import datetime
import sys


def print_info(*objs):
    print("INFO: ", *objs, file=sys.stderr)


class EnrollFormView(FormView):
    model = Recruit
    template_name = 'enrollment_form.html'
    fields = ['first_name', 'last_name', 'address1', 'address2', 'city',
        'state', 'zipcode', 'phone', 'realtor', 'ins_agent']
    form_class = RecruitModelForm
    recruit = None
    md5hash = None
    emailmessage = None

    def dispatch(self, request, *args, **kwargs):
        self.md5hash = self.kwargs.get('md5hash', '')
        try:
            self.emailmessage = EmailMessage.objects.get(url_key_code=self.md5hash)
            self.recruit = Recruit.objects.get(email=self.emailmessage.email)
        except:
            self.recruit = None

        # Keep record of when the form was opened.
        if self.emailmessage:
            MassEmailer.form_open_timestamp(self.emailmessage.id)

        return super(EnrollFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EnrollFormView, self).get_form_kwargs()
        if self.recruit:
            # Feed the form an existing record 'instance' to assure form.save()
            # is an update sql statement instead of insert.
            kwargs['instance'] = self.recruit
        return kwargs

    def get_initial(self):
        if self.recruit:
            return {
                'sponsor' : ' '.join([self.recruit.sponsor.first_name, self.recruit.sponsor.last_name]),
                'email' : self.recruit.email,
                'first_name' : self.recruit.first_name,
                'last_name' : self.recruit.last_name,
                'address1' : self.recruit.address1,
                'address2' : self.recruit.address2,
                'city' : self.recruit.city,
                'state' : self.recruit.state,
                'zipcode' : self.recruit.zipcode,
                'phone' : self.recruit.phone,
                'realtor' : self.recruit.realtor,
                'ins_agent' : self.recruit.ins_agent}
        else:
            return {
                'sponsor' : '',
                'email' : '',
                'first_name' : '',
                'last_name' : '',
                'address1' : '',
                'address2' : '',
                'city' : '',
                'state' : '',
                'zipcode' : '',
                'phone' : '',
                'realtor' : '',
                'ins_agent' : ''}

    def get_template_names(self):
        if self.recruit:
            return [self.template_name,]
        else:
            return ['enrollment_error.html',]

    def form_invalid(self, form):
        print_info('form.errors:')
        print_info(form.errors)

        ########## debugger on ##########
        #~ from pudb import set_trace; set_trace()
        return super(EnrollFormView, self).form_invalid(form)

    def form_valid(self, form):
        form.save()

        # Keep record of when the form was submitted.
        if self.emailmessage:
            MassEmailer.form_submit_timestamp(self.emailmessage.id)

        return super(EnrollFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EnrollFormView, self).get_context_data(**kwargs)
        if self.recruit:
            context['state_choices'] = STATE_CHOICES
            context['sponsor'] = ' '.join([self.recruit.sponsor.first_name, self.recruit.sponsor.last_name])
            context['md5hash'] = self.md5hash
        return context

    def get_success_url(self):
        return reverse_lazy('enroll-success', kwargs={'md5hash':self.md5hash})


class EnrollSuccessTemplateView(TemplateView):
    template_name = 'enrollment_success.html'
    recruit = None
    md5hash = None
    emailmessage = None

    def dispatch(self, request, *args, **kwargs):
        self.md5hash = self.kwargs.get('md5hash', '')
        try:
            self.emailmessage = EmailMessage.objects.get(url_key_code=self.md5hash)
            self.recruit = Recruit.objects.get(email=self.emailmessage.email)
        except:
            self.recruit = None

        return super(EnrollSuccessTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EnrollSuccessTemplateView, self).get_context_data(**kwargs)
        if self.recruit:
            context['sponsor'] = ' '.join([self.recruit.sponsor.first_name, self.recruit.sponsor.last_name])
        return context

    def get_template_names(self):
        if self.recruit:
            return [self.template_name,]
        else:
            return ['enrollment_error.html',]


class EnrollCancelTemplateView(TemplateView):
    template_name = 'enrollment_cancel.html'
    recruit = None
    md5hash = None
    emailmessage = None

    def dispatch(self, request, *args, **kwargs):
        self.md5hash = self.kwargs.get('md5hash', '')
        try:
            self.emailmessage = EmailMessage.objects.get(url_key_code=self.md5hash)
            self.recruit = Recruit.objects.get(email=self.emailmessage.email)
        except:
            self.recruit = None

        # Keep record of when the form entry was cancelled.
        if self.emailmessage:
            MassEmailer.form_cancel_timestamp(self.emailmessage.id)

        return super(EnrollCancelTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EnrollCancelTemplateView, self).get_context_data(**kwargs)
        if self.recruit:
            context['sponsor'] = ' '.join([self.recruit.sponsor.first_name, self.recruit.sponsor.last_name])
        return context

    def get_template_names(self):
        if self.recruit:
            return [self.template_name,]
        else:
            return ['enrollment_error.html',]


class EnrollTest2TemplateView(TemplateView):
    template_name = 'enrollment_form-2.html'

    def get_context_data(self, **kwargs):
        context = super(EnrollTest2TemplateView, self).get_context_data(**kwargs)
        context['state_choices'] = STATE_CHOICES
        return context
