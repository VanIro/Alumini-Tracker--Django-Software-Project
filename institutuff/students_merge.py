from django import forms
from records.forms import AlumniForm

student_basic_info_fields=[ 
    #'title',
    'first_name',
    'middle_name',
    'last_name',
    'dob_bs',
    'gender',

    'fathers_name',
    'mothers_name',
]

basic_info_opt=[
        'dob_bs','gender'
    ]
    
contact_info=[
        'contact_number','email','website','facebook_id','twitter_id','linked_in_id',
    ]

extra_info_choices=[
        'employment_status',
    ]

extra_info=[
        'currently_employed_organization', 'current_post_in_organization','comments'
    ]

student_education_fields=[
    "be_student_group","program", "program_type","batch_bs","roll_number", "ioe_roll number"
]


address_fields=[
        'address_type','country','state','district','city','vdc_municipality','ward_no','street_address',
    ]

further_academic_status_fields=[
        'level','status','program_name','country','institution','details'
    ]


class campus_education_form(forms.ModelForm):
    pass
    



def merge_student_entries(std1, std2):
    std1_form = AlumniForm(instance=std1)
    std2_form = AlumniForm(instance=std2)

    flag = True
    for key in student_basic_info_fields:
        if not std1_form[key] == std2_form[key]:
            flag=False
            break

    #bachelors
    for key in student_education_fields:
        key2 = 'be'+key
        if std1_form[key2] is None:
            pass 
        elif std2_form[key2] is None: 
           pass
        elif not std1_form[key2] == std2_form[key2]:
            flag=False

    #masters
    for key in student_education_fields[1:]:
        key2 = 'msc'+key
        if std1_form[key2] is None:
            pass 
        elif std2_form[key2] is None: 
           pass
        elif not std1_form[key2] == std2_form[key2]:
            flag=False

    #phd
    for key in student_education_fields[-3:]:
        key2 = 'phd'+key
        if std1_form[key2] is None:
            pass 
        elif std2_form[key2] is None: 
           pass
        elif not std1_form[key2] == std2_form[key2]:
            flag=False

    #
            


    pass