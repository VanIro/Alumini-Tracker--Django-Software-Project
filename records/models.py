from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django_countries.fields import CountryField


from django.core.exceptions import ValidationError

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Group

from .choices import GENDER_CHOICES, BE_PROGRAM_CHOICES, MSC_PROGRAM_CHOICES, BE_PROGRAM_TYPE_CHOICES, \
    MSC_PROGRAM_TYPE_CHOICES, TITLE_CHOICES, ADDRESS_TYPE_CHOICES, BE_STUDENT_GROUP_CHOICES,\
    ACADEMIC_LEVEL_CHOICES, ACADEMIC_STATUS_CHOICES, EMPLOYMENT_STATUS_CHOICES


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def validate_group(username):
    useru = User.objects.get(id=username)
    if not Group.objects.get(name='Students').user_set.all().filter(id=username).exists():
    #if not useru.groups.filter(name="Students").exists():
        raise ValidationError(
            (f'{useru.username} was not found to be a member of "Students".')
        )



class Student(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
    )

    # this field is not being used AFAIK, so data may not be correct
    # ie. some alumni may have this as False and vice-versa
    is_alumni = models.BooleanField(blank=False, null='False', default=False)

    user_account = models.OneToOneField(User,
        on_delete=models.SET(get_sentinel_user)
        ,validators=[validate_group], 
        null=True,blank=True,  
        related_name="student_user"
    )

    title = models.CharField(
        max_length=10,
        choices=TITLE_CHOICES,
        blank=True, null=True,
    )
    first_name = models.CharField(max_length=200, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=False)

    fathers_name = models.CharField(max_length=200, blank=True, null=True)
    mothers_name = models.CharField(max_length=200, blank=True, null=True)

    be_program = models.CharField(max_length=20, blank=True, null=True, default=None, choices=BE_PROGRAM_CHOICES)
    be_program_type = models.CharField(max_length=10, choices=BE_PROGRAM_TYPE_CHOICES, blank=True, null=True)
    be_batch_bs = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(4), MinLengthValidator(4)], blank=True, null=True, default=None)
    be_roll_number = models.CharField(max_length=3, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(3), MinLengthValidator(3)], blank=True, null=True, default=None)
    be_ioe_roll_number = models.CharField(max_length=50, blank=True, null=True, default=None)
    be_student_group = models.CharField(
        choices=BE_STUDENT_GROUP_CHOICES,
        blank=True,
        null=True,
        default=None,
        max_length=1,
    )

    msc_program = models.CharField(max_length=20, blank=True, null=True, default=None, choices=MSC_PROGRAM_CHOICES)
    msc_program_type = models.CharField(max_length=12, choices=MSC_PROGRAM_TYPE_CHOICES, blank=True, null=True)
    msc_batch_bs = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(4), MinLengthValidator(4)], blank=True, null=True, default=None)
    msc_roll_number = models.CharField(max_length=3, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(3), MinLengthValidator(3)], blank=True, null=True, default=None)
    msc_ioe_roll_number = models.CharField(max_length=50, blank=True, null=True, default=None)

    phd_batch_bs = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(4), MinLengthValidator(4)], blank=True, null=True, default=None)
    phd_roll_number = models.CharField(max_length=3, validators=[RegexValidator(r'^\d{1,10}$'), MaxLengthValidator(3), MinLengthValidator(3)], blank=True, null=True, default=None)
    phd_ioe_roll_number = models.CharField(max_length=50, blank=True, null=True, default=None)

    contact_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    facebook_id = models.CharField(max_length=200, blank=True, null=True)
    twitter_id = models.CharField(max_length=200, blank=True, null=True)
    linked_in_id = models.CharField(max_length=200, blank=True, null=True)

    areas_of_expertise = models.TextField(blank=True, null=True)

    dob_bs = models.CharField(max_length=10, validators=[RegexValidator(r'^20[0-9][0-9]/[0-9]{2}/[0-9]{2}$'), MaxLengthValidator(10), MinLengthValidator(10)], blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True, null=True,
    )

    recent_cv = models.FileField(
        upload_to='documents_cvs/',
        blank=True,
        null=True,
    )
    recent_passport_size_photo = models.FileField(
        upload_to="documents_photos/",
        blank=True,
        null=True,
    )

    employment_status = models.CharField(
        max_length=20,
        blank=True, null=True,
        choices=EMPLOYMENT_STATUS_CHOICES
    )
    currently_employed_organization = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )
    current_post_in_organization = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )

    comments = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['be_program', 'be_batch_bs', 'be_roll_number'], name="unique_be_credentials"),
            models.UniqueConstraint(fields=['msc_program', 'msc_batch_bs', 'msc_roll_number'], name="unique_msc_credentials"),
            models.UniqueConstraint(fields=['phd_batch_bs', 'phd_roll_number'], name="unique_phd_credentials"),
        ]

    def __str__(self):
        full_name = ""
        if self.first_name:
            full_name += self.first_name + " "
        if self.middle_name:
            full_name += self.middle_name + " "
        if self.last_name:
            full_name += self.last_name
        return full_name

    @property
    def full_name(self):
        return self.__str__()

    @property
    def full_roll_number(self):
        full_roll_num = ''
        be_enroll_data_complete = self.be_program and self.be_batch_bs and self.be_roll_number
        if be_enroll_data_complete:
            full_roll_num += f'{self.be_batch_bs[1:]}{self.be_program}{self.be_roll_number} '
        msc_enroll_data_complete = self.msc_program and self.msc_batch_bs and self.msc_roll_number
        if msc_enroll_data_complete:
            full_roll_num += f'{self.msc_batch_bs[1:]}{self.msc_program}{self.msc_roll_number} '
        phd_enroll_data_complete = self.phd_batch_bs and self.phd_roll_number
        if phd_enroll_data_complete:
            full_roll_num += f'{self.phd_batch_bs[1:]}PhD{self.phd_roll_number} '
        return full_roll_num

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        be_enroll_data_complete = self.be_program and self.be_batch_bs and self.be_roll_number
        # path('<batch_bs>/<program_code>/<roll_number>/update/', AlumniUpdateView.as_view(), name='record-update'),
        if be_enroll_data_complete:
            return reverse('record-update', kwargs={'batch_bs': self.be_batch_bs, 'program_code': self.be_program, 'roll_number':self.be_roll_number, 'last_name':self.last_name, 'dob_bs':self.dob_bs.replace('/', '') if self.dob_bs else ' '})
        msc_enroll_data_complete = self.msc_program and self.msc_batch_bs and self.msc_roll_number
        if msc_enroll_data_complete:
            return reverse('record-update', kwargs={'batch_bs': self.msc_batch_bs, 'program_code': self.msc_program, 'roll_number':self.msc_roll_number, 'last_name':self.last_name, 'dob_bs':self.dob_bs.replace('/', '') if self.dob_bs else ' '})
        phd_enroll_data_complete = self.phd_batch_bs and self.phd_roll_number
        if phd_enroll_data_complete:
            return reverse('record-update', kwargs={'batch_bs': self.phd_batch_bs, 'roll_number':self.phd_roll_number, 'last_name':self.last_name, 'dob_bs':self.dob_bs.replace('/', '') if self.dob_bs else ' '})
        return reverse('alumni-login')

    def save(self, *args, **kwargs):
        self.slug = self.full_roll_number

        return super(Student, self).save(*args, **kwargs)

    def clean(self):

        attributes_to_change_to_none_if_empty = [
            'be_program', 'be_batch_bs', 'be_roll_number',
            'msc_program', 'msc_batch_bs', 'msc_roll_number',
            'phd_batch_bs', 'phd_roll_number',
        ]

        for attribute_name in attributes_to_change_to_none_if_empty:
            if getattr(self, attribute_name) == "":
                setattr(self, attribute_name, None)

        be_enroll_data_complete = self.be_program and self.be_batch_bs and self.be_roll_number
        msc_enroll_data_complete = self.msc_program and self.msc_batch_bs and self.msc_roll_number
        phd_enroll_data_complete = self.phd_batch_bs and self.phd_roll_number

        if not (be_enroll_data_complete or msc_enroll_data_complete or phd_enroll_data_complete):
            raise ValidationError('Program(if applicable), Batch, and Roll number of at least one enrolled program has to be complete')


    # def save(self, *args, **kwargs):
    #     super().save(*args, *kwargs)
    #     print("File saved at " + self.file.path)


class Address(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'address_type'], name="unique_student_and_address_type"),
        ]

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='has_addresses'
    )
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES,
        blank=False,
    )

    country = CountryField(blank_label='(select country)', blank=False)
    state = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    vdc_municipality = models.CharField(max_length=50, blank=True, null=True)
    ward_no = models.IntegerField(blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)	
    
    def clean(self):
        attributes_to_change_to_none_if_empty = [
            'state', 'district', 'city', 'vdc_municipality', 'ward_no','street_address',
        ]

        for attribute_name in attributes_to_change_to_none_if_empty:
            if getattr(self, attribute_name) == "":
                setattr(self, attribute_name, None)

        data_complete = self.country and self.address_type

        if not data_complete:
            raise ValidationError('Minimum of address type and country needed for Address')



class FurtherAcademicStatus(models.Model):
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='has_further_academic_statuses'
    )
    level = models.CharField(
        max_length=20,
        blank=False,
        choices=ACADEMIC_LEVEL_CHOICES,
    )
    status = models.CharField(
        max_length=20,
        blank=True,
        choices=ACADEMIC_STATUS_CHOICES,
    )
    program_name = models.CharField(max_length=100, blank=True)
    country = CountryField(blank_label='(select country)', blank=True)
    institution = models.CharField(max_length=100,blank=True)
    details = models.CharField(
        max_length=200,
        blank=True,
    )
