from django.contrib import admin
from .models import VisaType, Occupation, MonthYear, VisaData


@admin.register(VisaType)
class VisaTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(MonthYear)
class MonthYearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)


@admin.register(VisaData)
class VisaDataAdmin(admin.ModelAdmin):
    list_display = ('month_year', 'visa_type', 'occupation', 'status', 'points', 'count')
    list_filter = ('visa_type', 'status', 'month_year', 'points')
    search_fields = ('visa_type__name', 'occupation__name')
    list_select_related = ('month_year', 'visa_type', 'occupation')
    ordering = ('-month_year__name', 'visa_type__name', 'occupation__name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('month_year', 'visa_type', 'occupation')
        }),
        ('Details', {
            'fields': ('status', 'points', 'count')
        }),
    )

    list_per_page = 50
