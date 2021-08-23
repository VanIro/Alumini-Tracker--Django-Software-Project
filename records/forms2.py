from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from .models import Student, Address, FurtherAcademicStatus
from .choices import PROGRAM_LEVEL_CHOICES, \
    BE_PROGRAM_CHOICES, MSC_PROGRAM_CHOICES, GROUPED_PROGRAM_CHOICES
from django.db.models import Q
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, Column, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

import re

from allauth.account.forms import SignupForm

be_programs_list = [program[0] for program in BE_PROGRAM_CHOICES]
msc_programs_list = [program[0] for program in MSC_PROGRAM_CHOICES]
phd_programs_list = ['PhD']

class Alumni_signup_form(SignupForm):
    program = forms.ChoiceField(choices=GROUPED_PROGRAM_CHOICES)
    batch_bs = forms.CharField(
        widget=forms.TextInput(),
        max_length=4,
        min_length=4,
        validators=[RegexValidator(r'^\d{1,10}$'),],
        label='Batch (in BS)',
        help_text='Example- 2055',
    )
    roll_number = forms.CharField(
        widget=forms.TextInput(),
        max_length=3,
        min_length=3,
        validators=[RegexValidator(r'^\d{1,10}$'),],
        label='Roll Number',
        help_text='Example- 601',
    )
    last_name = forms.CharField(
    	widget = forms.TextInput(),
        max_length=50,
        label='Last Name',
    )
    dob_bs = forms.CharField(
        widget=forms.TextInput(),
        max_length=10,
        min_length=10,
        label='Date Of Birth (in BS)',
        help_text='Example- 2055/01/01',
    )
    #field_order = ['program','batch','last_name','roll_number','dob_bs','email','password']
    #fields = ['program','batch','last_name','roll_number','dob_bs','email','password']
    
    #def signup(self, request, user):
    #    super(Alumni_signup_form,self).save(request)
    #    pass
    

            
    def save(self,request):
        user=super(Alumni_signup_form,self).save(request)
        Group.objects.get(name='Students').user_set.add(user) 
        self.queried_student.user_account = user
        self.queried_student.save()
        messages.add_message(request,messages.INFO,"%s has been given this account"%user.student_user.first_name)
        return user
    
    def is_valid(self):
        if not super(Alumni_signup_form,self).is_valid():
            return False
        try:
            program = self.data.get('program')
            batch_bs = self.data.get('batch_bs')
            roll_number = self.data.get('roll_number')
            last_name = self.data.get('last_name').strip()
            dob_bs = self.data.get('dob_bs')
            if program in be_programs_list:
                query = Student.objects.filter(Q( be_batch_bs__exact=batch_bs,last_name__iexact=last_name,
                                              be_roll_number__exact=roll_number, dob_bs__isnull=True
                                              ) |
                                          Q(be_batch_bs__exact=batch_bs,last_name__iexact=last_name, 
                                            be_roll_number__exact=roll_number, dob_bs__exact=dob_bs
                                            ))
                #if query.exists():
                #    return True
            elif program in msc_programs_list:
                query = Student.objects.filter(Q( msc_batch_bs__exact=batch_bs,last_name__iexact=last_name,
                                              msc_roll_number__exact=roll_number, dob_bs__isnull=True
                                              ) |
                                          Q(msc_batch_bs__exact=batch_bs,last_name__iexact=last_name, 
                                            msc_roll_number__exact=roll_number, dob_bs__exact=dob_bs
                                            ))
                #if query.exists():    
                #    return True
            elif program in phd_programs_list:
                query = Student.objects.filter(Q( phd_batch_bs__exact=batch_bs,last_name__iexact=last_name,
                                              phd_roll_number__exact=roll_number, dob_bs__isnull=True
                                              ) |
                                          Q(phd_batch_bs__exact=batch_bs,last_name__iexact=last_name, 
                                            phd_roll_number__exact=roll_number, dob_bs__exact=dob_bs
                                            ))
                #if query.exists():
                #    return True
            else:
                return False
            
            #raise ValidationError("ynha chai aayo...")
            if query.exists():
                self.queried_student = query.get() 
                #if self.queried_student.user_account:
                #    messages.INFO("this user has already registered")
                #    return False
                return True
        except(ValueError, TypeError):
            return False

    def clean(self):
        super(Alumni_signup_form,self).clean()
        return self.cleaned_data
        #cleaned_data = super(Alumni_signup_form,self).clean()
        #return cleaned_data
    def __init__(self, *args, **kwargs):
        super(Alumni_signup_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('program'),
                Field('batch_bs'),
                Field('roll_number'),
	 	        Field('last_name'),
                Field('dob_bs'),
                Field('email'),
                Field('password1'),
                Field('password2'),
                HTML('<br><div style="text-align:left;">'),
                ButtonHolder(
                    Submit('submit', 'Sign Up')
                ),
                HTML('</br>'),
            )
        )

class email_form(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(),
        max_length=200,
        label='Subject',
        #help_text='subject...',
    )
    message = forms.CharField(
        widget=forms.Textarea(),
        label='message',
        #help_text='your message',
    )
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('subject'),
                Field('message'),
                HTML('<br><div style="text-align:left;">'),
                ButtonHolder(
                    Submit('submit', 'Send')
                ),
                HTML('</br>'),
            )
        )
        # btn   btn - outline - info
        super(email_form, self).__init__(*args, **kwargs)


        