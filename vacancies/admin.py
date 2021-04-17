from django.contrib import admin

from .models import Company, Specialty, Vacancy, Application

class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'location', 'logo', 'description', 'employee_count')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty)
admin.site.register(Vacancy)
admin.site.register(Application)