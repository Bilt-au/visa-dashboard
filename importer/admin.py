from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import ExcelImport
from .services import ExcelImportService
import os


@admin.register(ExcelImport)
class ExcelImportAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_at', 'processed', 'status_display', 'actions_display')
    list_filter = ('processed', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'processed', 'total_rows', 'processed_rows', 'errors_count', 'errors_detail')
    search_fields = ('file',)
    ordering = ['-uploaded_at']

    fieldsets = (
        ('Upload', {
            'fields': ('file',)
        }),
        ('Processing Status', {
            'fields': ('uploaded_at', 'processed', 'total_rows', 'processed_rows', 'errors_count'),
            'classes': ('collapse',)
        }),
        ('Error Details', {
            'fields': ('errors_detail',),
            'classes': ('collapse',)
        }),
    )

    def file_name(self, obj):
        return os.path.basename(obj.file.name) if obj.file else 'No file'
    file_name.short_description = 'File Name'

    def status_display(self, obj):
        if not obj.processed:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
        elif obj.errors_count and obj.errors_count > 0:
            return format_html('<span style="color: red;">❌ Completed with errors</span>')
        else:
            return format_html('<span style="color: green;">✅ Completed successfully</span>')
    status_display.short_description = 'Status'

    def actions_display(self, obj):
        if not obj.processed:
            process_url = reverse('admin:process_import', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">Process Import</a>',
                process_url
            )
        else:
            return "Processed"
    actions_display.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'process/<int:import_id>/',
                self.admin_site.admin_view(self.process_import),
                name='process_import',
            ),
        ]
        return custom_urls + urls

    def process_import(self, request, import_id):
        try:
            excel_import = ExcelImport.objects.get(id=import_id)

            if excel_import.processed:
                messages.warning(request, f'Import {import_id} has already been processed.')
                return HttpResponseRedirect(reverse('admin:importer_excelimport_changelist'))

            # Process the file
            service = ExcelImportService()
            results = service.process_excel_file(excel_import.file.path)

            # Update the import record
            excel_import.processed = True
            excel_import.total_rows = results['total_rows']
            excel_import.processed_rows = results['processed']
            excel_import.errors_count = len(results['errors'])
            excel_import.errors_detail = '\n'.join(results['errors']) if results['errors'] else ''
            excel_import.save()

            if results['errors']:
                messages.warning(
                    request,
                    f'Import completed with {len(results["errors"])} errors. '
                    f'Processed {results["processed"]} out of {results["total_rows"]} rows.'
                )
            else:
                messages.success(
                    request,
                    f'Import completed successfully! Processed {results["processed"]} rows.'
                )

        except ExcelImport.DoesNotExist:
            messages.error(request, f'Import {import_id} not found.')
        except Exception as e:
            messages.error(request, f'Error processing import: {str(e)}')

        return HttpResponseRedirect(reverse('admin:importer_excelimport_changelist'))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only for new uploads
            messages.info(
                request,
                f'File uploaded successfully. Click "Process Import" to import the data.'
            )
