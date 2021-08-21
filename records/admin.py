from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from import_export.admin import ExportActionModelAdmin
from import_export import resources
from .models import Student, Address, FurtherAcademicStatus

from .admin_view import send_email_admin_init
# Register your models here.


class AddressInline(admin.TabularInline):
    model = Address


class AcademicStatusInline(admin.TabularInline):
    model = FurtherAcademicStatus


def make_alumni(modeladmin, request, queryset):
    queryset.update(is_alumni = True)

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student



class StudentAdmin(AdminAdvancedFiltersMixin, ExportActionModelAdmin):
    def __init__(self,*args,**kwargs):
        super(StudentAdmin,self).__init__(*args,**kwargs)
        #self.actions = super(StudentAdmin,self).actions
        self.actions = self.actions + self.added_actions

    #def save_model(self, request, obj, form, change):
    #    obj.uploader = request.user
    #    return super().save_model(request, obj, form, change)

    #def get_readonly_fields(self,request, obj=None):
    #    if obj is None:  # add form
    #        return self.readonly_fields
    #    else:
    #        return self.readonly_fields + ('uploader')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'uploader':
            # setting the user from the request object
            kwargs['initial'] = request.user.id
            # making the field readonly
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    added_actions=[send_email_admin_init]
    inlines = [
        AddressInline,
        AcademicStatusInline,
    ]
    resource_class = StudentResource
    list_display = (
        'full_name',
        'full_roll_number',
        'email',
        'contact_number',
        'date_modified',
    )
    ordering = (
        'be_program',
        'be_batch_bs',
        'be_roll_number',
        'msc_program',
        'msc_batch_bs',
        'msc_roll_number',
        'phd_batch_bs',
        'phd_roll_number',
    )
    search_fields = (
        'first_name',
        'middle_name',
        'last_name',
        'be_program',
        'be_batch_bs',
        'be_roll_number',
        'msc_program',
        'msc_batch_bs',
        'msc_roll_number',
        'phd_batch_bs',
        'phd_roll_number',
    )
    list_filter = (
        'be_program',
        'be_batch_bs',
        'msc_program',
        'msc_batch_bs',
        'phd_batch_bs',
    )
    advanced_filter_fields = (
        'title',
        'first_name',
        'middle_name',
        'last_name',
        'fathers_name',
        'mothers_name',
        'be_program',
        'be_program_type',
        'be_batch_bs',
        'be_roll_number',
        'be_ioe_roll_number',
        'be_student_group',
        'msc_program',
        'msc_program_type',
        'msc_batch_bs',
        'msc_roll_number',
        'msc_ioe_roll_number',
        'phd_batch_bs',
        'phd_program_type',
        'phd_roll_number',
        'phd_ioe_roll_number',
        'contact_number',
        'email',
        'website',
        'facebook_id',
        'twitter_id',
        'linked_in_id',
        'areas_of_expertise',
        'dob_bs',
        'gender',

        ('employment_status', 'Employment - status'),
        ('currently_employed_organization', 'Employment - organization'),
        ('current_post_in_organization', 'Employment - Post'),

        ('has_addresses__address_type', 'address - address_type'),
        ('has_addresses__country', 'address - country'),
        ('has_addresses__state', 'address - state'),
        ('has_addresses__district', 'address - district'),
        ('has_addresses__city', 'address - city'),
        ('has_addresses__vdc_municipality', 'address - vdc/municipality'),
        ('has_addresses__ward_no', 'address - ward_no'),

        ('has_further_academic_statuses__level', 'Further Academics - level'),
        ('has_further_academic_statuses__status', 'Further Academics - status'),
        ('has_further_academic_statuses__details', 'Further Academics - details'),
    )


admin.site.register(Student, StudentAdmin)
