from django.contrib import admin
from .models import Bed,Doctor,Patient

@admin.register(Bed)
class Bed(admin.ModelAdmin):
    list_display=('bed_number','occupied')
    list_display_links=('bed_number',)
@admin.register(Doctor)
class doctorsAdmin(admin.ModelAdmin):
    list_display=('name',)
    list_display_links=('name',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=('name','phone_num','patient_relative_name','patient_relative_contact','address','symptoms','prior_aliments','bed_num','dob','doctor','status')
    list_display_links=('name',)

