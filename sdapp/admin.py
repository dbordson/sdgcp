from django.contrib import admin

# Register your models here.
from .models import IssuerCIK, ReportingPerson


class ReportingPersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['person_name']}),
        (None,              {'fields': ['reporting_owner_cik_num']})
    ]
    search_fields = ['person_name']

admin.site.register(IssuerCIK)
admin.site.register(ReportingPerson, ReportingPersonAdmin)
