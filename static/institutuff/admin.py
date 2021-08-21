from django.contrib import admin
from .models import Institute

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display=(
            'full_name',
            'position_in_institution',
            'email',
            'userName',
        )

# Register your models here.
