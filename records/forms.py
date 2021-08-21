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

import re


be_programs_list = [program[0] for program in BE_PROGRAM_CHOICES]
msc_programs_list = [program[0] for program in MSC_PROGRAM_CHOICES]
phd_programs_list = ['PhD']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ()
        labels = {
            'address_type': 'Type',
            'vdc_municipality': 'VDC/Municipality',
            'ward_no': 'Ward No.',
        }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        # since csrf enabled by default for alumni form
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('address_type', css_class='form-group col-md-3 mb-0'),
                    Column('country', css_class='form-group col-md-3 mb-0'),
                    Column('state', css_class='form-group col-md-2 mb-0'),
                    Column('district', css_class='form-group col-md-3 mb-0'),
                    Column('city', css_class='form-group col-md-3 mb-0'),
                    Column('vdc_municipality', css_class='form-group col-md-3 mb-0'),
                    Column('ward_no', css_class='form-group col-md-2 mb-0'),
		            Column('street_address', css_class='form-group col-md-8 mb-0'),
                    Column('DELETE', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row formset_row-{}'.format(formtag_prefix)
                ),
                css_class='container ml-3',
            ),
            HTML("<br><hr>"),
        )


AddressFormSet = inlineformset_factory(
    Student, Address, form=AddressForm,
    fields=['address_type', 'country', 'state', 'district', 'city', 'vdc_municipality', 'ward_no', 'street_address',],
    extra=2,
    max_num=2,
    can_delete=True,
)


class FurtherAcademicStatusForm(forms.ModelForm):
    class Meta:
        model = FurtherAcademicStatus
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        # since csrf enabled by default for alumni form
        self.helper.disable_csrf=True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('level', css_class='form-group col-md-3 mb-0'),
                    Column('status', css_class='form-group col-md-3 mb-0'),
                    Column('country', css_class='form-group col-md-4 mb-0'),
                    Column('institution', css_class='form-group col-md-6 mb-0'),
                    Column('program_name', css_class='form-group col-md-6 mb-0'),
                    Column('details', css_class='form-group col-md-8 mb-0'),
                    Column('DELETE', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row formset_row-{}'.format(formtag_prefix)
                ),
                css_class='container ml-3'
            ),
            HTML("<br><hr>"),
        )


FurtherAcademicStatusFormSet = inlineformset_factory(
    Student, FurtherAcademicStatus, form=FurtherAcademicStatusForm,
    fields=['level', 'status', 'program_name', 'country', 'institution', 'details', ],
    extra=1,
    can_delete=True,
)


class AlumniForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['uploader', 'date_added', 'is_alumni',]
        labels = {
            'dob_bs': 'Date Of Birth (in BS)',
            'recent_cv': 'Recent CV',
            'recent_passport_size_photo':'Recent Passport Size Photo',
            'fathers_name': "Father's name",
            'mothers_name': "Mother's name",
            'currently_employed_organization': 'Organization',
            'current_post_in_organization': 'Post/Position',
        }
        help_texts = {
            'dob_bs': 'Example- 2055/01/01',
            'recent_passport_size_photo': 'For Alumni yearbook (Aspect ratio 1:1 recommended)',
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Fieldset(
                "Basic Info",
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'dob_bs',
                'gender',

                'fathers_name',
                'mothers_name',
            ),

            HTML("<br><hr>"),

            Fieldset(
                "Contact Info",
                'contact_number',
                'email',
                'website',
                'facebook_id',
                'twitter_id',
                'linked_in_id',

                'areas_of_expertise',
                'recent_cv',
                'recent_passport_size_photo',
            ),

            HTML("<br><hr>"),

            Fieldset(
                "Current Employment Details",
                'employment_status',
                'currently_employed_organization',
                'current_post_in_organization',
            ),
            HTML("<br><hr>"),

            Fieldset('Address',
                     HTML("<p>Please add/correct details of your current and permanent addresses.<br>"
                          "You can press 'remove' to remove data<br></p>"),
                     Formset('addresses')),

            Fieldset('Further Academics',
                     HTML("<p>Please add details of all further studies, both in DOECE and otherwise<br>"
			  "If the further study is at DOECE, Pulchowk, please mention DOECE in the institution name,<br> "
			  "enrolled program in Program name and Roll number in the Details so that your records can be merged by the admin.<br>"
                          "You can press 'add another' for more data and 'remove' to remove data<br></p>"),
                     Formset('furtheracademicstatus')),

            Field('comments'),
            HTML("<br>"),
            ButtonHolder(Submit('submit', 'Save')),
        )

        super(AlumniForm, self).__init__(*args, **kwargs)

        # make compulsary in form but not in model
        self.fields['email'].required = True
        self.fields['dob_bs'].required = True


class LoginForm(forms.Form):

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

    def __init__(self, *args, **kwargs):
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
            program = self.data.get('program')
            level_id = self.data.get('program_level')
            batch_bs = self.data.get('batch_bs')
            roll_number = self.data.get('roll_number')
            last_name = self.data.get('last_name').strip()
            dob_bs = self.data.get('dob_bs')
            if program in be_programs_list:
                if Student.objects.filter(Q(last_name__iexact=last_name, be_batch_bs__exact=batch_bs,
                                              be_roll_number__exact=roll_number, dob_bs__isnull=True) |
                                          Q(last_name__iexact=last_name, be_batch_bs__exact=batch_bs,
                                            be_roll_number__exact=roll_number, dob_bs__exact=dob_bs)).exists():
                    return True
            elif program in msc_programs_list:
                if Student.objects.filter(Q(last_name__iexact=last_name, msc_batch_bs__exact=batch_bs,
                                              msc_roll_number__exact=roll_number, dob_bs__isnull=True) |
                                          Q(last_name__iexact=last_name, msc_batch_bs__exact=batch_bs,
                                            msc_roll_number__exact=roll_number, dob_bs__exact=dob_bs)).exists():
                    return True
            elif program in phd_programs_list:
                if Student.objects.filter(Q(last_name__iexact=last_name, phd_batch_bs__exact=batch_bs,
                                              phd_roll_number__exact=roll_number, dob_bs__isnull=True) |
                                          Q(last_name__iexact=last_name, phd_batch_bs__exact=batch_bs,
                                            phd_roll_number__exact=roll_number, dob_bs__exact=dob_bs)).exists():
                    return True
            else:
                return False
        except(ValueError, TypeError):
            return False

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()


class YearbookViewForm(forms.Form):
    program = forms.ChoiceField(choices=GROUPED_PROGRAM_CHOICES)
    batch_bs = forms.CharField(
        widget=forms.TextInput(),
        max_length=4,
        min_length=4,
        validators=[RegexValidator(r'^\d{1,10}$'),],
        label='Batch (in BS)',
        help_text='Example- 2055',
        initial='2055',
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4 create-label'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Div(
                Field('program'),
                Field('batch_bs'),
                HTML('<br><div style="text-align:center;">'),
                ButtonHolder(
                    Submit('submit', 'View yearbook')
                ),
                HTML('</br>'),
            )
        )
        super(YearbookViewForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        try:
            program = self.data.get('program')
            batch_bs = self.data.get('batch_bs')
            if program in be_programs_list:
                if Student.objects.filter(Q(be_program__exact=program, be_batch_bs__exact=batch_bs)).exists():
                    return True
            elif program in msc_programs_list:
                if Student.objects.filter(Q(msc_program__exact=program, msc_batch_bs__exact=batch_bs)).exists():
                    return True
            elif program in phd_programs_list:
                if Student.objects.filter(Q(phd_batch_bs__exact=batch_bs)).exists():
                    return True
            else:
                return False
        except(ValueError, TypeError):
            return False

    # def is_valid(self):
    #     try:
    #         program = self.data.get('program')
    #         batch_bs = self.data.get('batch_bs')
    #     except(ValueError, TypeError):
    #         return False
