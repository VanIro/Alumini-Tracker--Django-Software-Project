from django.db.models import Q
from records.models import Student
from records.models import Address
from records.choices import PROGRAM_LEVEL_CHOICES
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django_countries import countries
import django_filters

class StudentFilter(django_filters.FilterSet):
    batch = django_filters.CharFilter(method='check_batch', label='batch/year')
    program = django_filters.CharFilter(method='check_program', label='program code')
    level = django_filters.CharFilter(method='check_level',label='level')#, choices=PROGRAM_LEVEL_CHOICES)
    country = django_filters.CharFilter(method='check_country',label='country')

    def check_batch(self, queryset, name, value):
        return queryset.filter(
                Q(be_batch_bs=value)|Q(msc_batch_bs=value)|Q(phd_batch_bs=value)
            )
    def check_program(self, queryset, name, value):
        return queryset.filter(
                Q(be_program__iexact=value)|Q(msc_program__iexact=value)
            )
    def check_level(self, queryset, name, value):
        choices = [x[0] for x in PROGRAM_LEVEL_CHOICES]
        if value.lower()==choices[0].lower() :
            return queryset.filter(
                    Q(be_roll_number__isnull=False)
                )
        elif value.lower()==choices[1].lower() :
            return queryset.filter(
                    Q(msc_roll_number__isnull=False)
                )
        elif value.lower()==choices[2].lower() :
            return queryset.filter(
                    Q(phd_roll_number__isnull=False)
                )
    #is this check_country efficient?
    def check_country(self, queryset, name, value):
        dict_req = dict(countries)
        dict_values = [val.lower() for val in list(dict_req.values())]
        try:
            code=list(dict_req.keys())[dict_values.index(value.lower())]
        except ValueError:
            return Student.objects.none()

        qset=Address.objects.filter(country__iexact=code).select_related('student')
        if not qset.exists():
            return Student.objects.none()
        list_stdnt = [a.student.id for a in qset] 
        #raise ValidationError(list_stdnt)
        return Student.objects.filter(id__in=list_stdnt)


    class Meta:
        model=Student
        fields=['batch','program']
