from django.db.models import Q
from records.models import Student
from records.choices import PROGRAM_LEVEL_CHOICES
import django_filters

class StudentFilter(django_filters.FilterSet):
    batch = django_filters.CharFilter(method='check_batch', label='batch/year')
    program = django_filters.CharFilter(method='check_program', label='program code')
    level = django_filters.CharFilter(method='check_level',label='level')#, choices=PROGRAM_LEVEL_CHOICES)
    
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

    class Meta:
        model=Student
        fields=['batch','program']
