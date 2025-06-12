from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Phone
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import HttpResponse
import io
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def phone_list(request):
    companies = Company.objects.all().order_by('name')
    return render(request, 'phone_list.html', {'companies': companies})

def phone_detail(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    return render(request, 'phone_detail.html', {'phone': phone})

def compare(request):
    phones = Phone.objects.select_related('company').all().order_by('company__name', 'model')
    phone1 = phone2 = None
    all_keys = []
    phone1_id = request.GET.get('phone1')
    phone2_id = request.GET.get('phone2')
    if phone1_id and phone2_id and phone1_id != phone2_id:
        phone1 = get_object_or_404(Phone, pk=phone1_id)
        phone2 = get_object_or_404(Phone, pk=phone2_id)
        all_keys = sorted(set(phone1.specs.keys()) | set(phone2.specs.keys()))
    return render(request, 'compare.html', {
        'phones': phones,
        'phone1': phone1,
        'phone2': phone2,
        'all_keys': all_keys,
    })

def how_to_use(request):
    return render(request, 'static_pages/how_to_use.html')

def terms(request):
    return render(request, 'static_pages/terms.html')

def privacy(request):
    return render(request, 'static_pages/privacy.html')

# Custom template filter for dict key access
from django import template
register = template.Library()
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@staff_member_required
def backup(request):
    buf = io.StringIO()
    call_command('dumpdata', stdout=buf)
    response = HttpResponse(buf.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response

@staff_member_required
def restore(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        call_command('loaddata', request.FILES['json_file'])
        messages.success(request, 'Database restored!')
        return redirect('admin:index')
    return render(request, 'admin/restore.html')
