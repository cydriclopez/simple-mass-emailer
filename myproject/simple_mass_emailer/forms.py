
from django import forms
from .models import Recruit


class RecruitModelForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ['first_name', 'last_name', 'address1',
                'address2', 'city', 'state', 'zipcode', 'phone', 'realtor', 'ins_agent']
