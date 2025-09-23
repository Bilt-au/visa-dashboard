from django.db import models


class ExcelImport(models.Model):
    file = models.FileField(upload_to='imports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    total_rows = models.IntegerField(null=True, blank=True)
    processed_rows = models.IntegerField(null=True, blank=True)
    errors_count = models.IntegerField(null=True, blank=True)
    errors_detail = models.TextField(blank=True)

    class Meta:
        verbose_name = "Excel Import"
        verbose_name_plural = "Excel Imports"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Import {self.id} - {self.file.name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
