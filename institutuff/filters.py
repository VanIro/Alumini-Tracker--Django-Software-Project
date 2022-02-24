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
    name = django_filters.CharFilter(method='check_name',label='Name')

    def check_batch(self, queryset, name, value):
        #raise ValidationError(list(queryset.filter( Q(be_batch_bs=value)|Q(msc_batch_bs=value)|Q(phd_batch_bs=value) )))
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
        else : 
            return Student.objects.none()
    #is this check_country efficient?
    def check_country(self, queryset, name, value):
        dict_req = dict(countries)
        dict_values = [val.lower() for val in list(dict_req.values())]
        try:
            code=list(dict_req.keys())[dict_values.index(value.lower())]
        except ValueError:
            return Student.objects.none()

        qset=Address.objects.filter( id__in = queryset.values('has_addresses__id') )\
                                .filter(country__iexact=code).select_related('student')
        if not qset.exists():
            return Student.objects.none()
        list_stdnt = [a.student.id for a in qset] 
        #raise ValidationError(list_stdnt)
        return Student.objects.filter(id__in=list_stdnt)

    def Q_check_list_in_field(self,q_list,field_name='last_name'):
        #this type of query can be optimised if in the search field, multiple whitespaces in between the words are cleaned
        #with:
        #"".join([ s+" " for s in q_list ]).rstrip() instead of the loop
        query = Q()
        for s in q_list:
            query = query & Q(**{field_name+"__icontains":s})
        return query

    def check_name(self, queryset, name, value):
        #aali sochya vanda badhi complex huna pugyo yo function chai :{
        name_words = str(value).split()
        len_name_words = len(name_words)

        #len_name_words will never be zero

        #(F,M)1,L,(FM)2,FL,ML,FML

        query_0 = Q(first_name__iexact=name_words[0]) 

        query = Q()
        if len_name_words==1:
            #F,M
            query = query_0 |Q(middle_name__iexact=name_words[0]) 
        
        last_name_possibly_L=name_words
        ##last_name_possibly = "".join([ s+" " for s in name_words ]).rstrip()
        #L
        query = query | self.Q_check_list_in_field(last_name_possibly_L)#Q(last_name__icontains=last_name_possibly) 
        if len_name_words>1:
            if len_name_words==2: 
                #FM
                query = query | ( query_0 & Q(middle_name__iexact=name_words[1]) ) 
            first = last_name_possibly_L.pop(0)
            ##first, last_name_possibly = last_name_possibly.split(" ",1)
            #FL
            query = query | \
                        ( Q(first_name__iexact=first) & self.Q_check_list_in_field(last_name_possibly_L) )#Q(last_name__icontains=last_name_possibly)  )
            #ML
            query = query | \
                        ( Q(middle_name__iexact=first) & self.Q_check_list_in_field(last_name_possibly_L) )#Q(last_name__icontains=last_name_possibly)  )
            if len_name_words>2:
                middle = last_name_possibly_L.pop(0)
                ##middle, last_name_possibly = last_name_possibly.split(" ",1)
                #FML
                query = query | \
                            ( Q(first_name__iexact=first) & Q(middle_name__iexact=middle) & self.Q_check_list_in_field(last_name_possibly_L) )#Q(last_name__icontains=last_name_possibly)  )

        #print(query)
        return queryset.filter(query)


    class Meta:
        model=Student
        fields=['batch','program']
