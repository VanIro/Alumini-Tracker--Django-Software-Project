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

student_bachelor_education_fields=[
    "program", "program type","batch bs","roll number", "ioe roll number", "student group"
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


    pass