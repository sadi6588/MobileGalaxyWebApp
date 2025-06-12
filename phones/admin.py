import csv
from django.http import HttpResponse
from django.contrib import admin, messages
from .models import Company, Phone
from django.shortcuts import redirect, render
from django.urls import path
from django import forms
import io
import json

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('company', 'model')
    search_fields = ('model',)
    list_filter = ('company',)
    actions = ['export_as_csv']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='phones_phone_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = io.TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)
                for row in reader:
                    company, _ = Company.objects.get_or_create(name=row['company'])
                    specs = json.loads(row['specs']) if 'specs' in row and row['specs'] else {}
                    Phone.objects.create(
                        company=company,
                        model=row['model'],
                        specs=specs,
                    )
                self.message_user(request, "Phones imported successfully!", messages.SUCCESS)
                return redirect("..")
        else:
            form = CsvImportForm()
        context = self.admin_site.each_context(request)
        context['form'] = form
        context['opts'] = self.model._meta
        context['title'] = "Import Phones from CSV"
        return render(request, "admin/import_csv.html", context)

    def export_as_csv(self, request, queryset):
        field_names = ['company', 'model', 'specs']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=phones.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([
                obj.company.name,
                obj.model,
                json.dumps(obj.specs)
            ])
        return response
    export_as_csv.short_description = "Export Selected to CSV"
