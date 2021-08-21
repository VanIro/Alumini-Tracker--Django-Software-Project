"""
used in forms.py(AlumniForm) for filling up Address, and FurtherAcademicStatus, while filling up a form for
a Student.
Used for front-end part of the form only
ass such functionality already in django-admin
"""

from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from django.shortcuts import render
from django.template.loader import render_to_string


class Formset(LayoutObject):
    template = "records/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})