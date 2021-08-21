from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from .models import Institute
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, Column, HTML, ButtonHolder, Submit
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

class LoginForm(forms.Form):
    last_name = forms.CharField(
    	widget = forms.TextInput(),
        max_length=50,
        label='Last Name',
    )
    #position_in_institution = forms.CharField(
    #    widget = forms.TextInput(),
    #    max_length=100
    #)
    id_code = forms.CharField(
    	widget = forms.TextInput(),
        max_length=15,
        label='id_code',
    )
    userName = forms.CharField(
        widget = forms.TextInput(),
        min_length = 5,
        max_length = 30,
        label = 'username',
    )
    password = forms.CharField(
        widget = forms.PasswordInput(),
        min_length = 5,
        max_length = 30,
        label = 'password',
    )
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
		        Field('last_name'),
                Field('id_code'),
                Field('userName'),
                Field('password'),
                HTML('<br><div style="text-align:center;">'),
                ButtonHolder(
                    Submit('submit', 'Login')
                ),
                HTML('</br>'),
            )
        )
        # btn   btn - outline - info
        super(LoginForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        try:
            last_name = self.data.get('last_name')
            id_code = self.data.get('id_code')
            userName = self.data.get('userName')
            #pos_in_inst = self.data.get('position_in_institution')
            try:
                user = User.objects.get(username=userName)
                if Institute.objects.filter(
                    Q(last_name__iexact = last_name, id_code = id_code, userName =user)    
                ).exists():
                    return True
            except ObjectDoesNotExist:
                return False
            else:
                return False
        except(ValueError, TypeError):
            return False
