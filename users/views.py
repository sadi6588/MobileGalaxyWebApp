from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import base64
from io import BytesIO

# Create your views here.

@login_required
def profile(request):
    # 2FA setup for admin
    device = None
    qr_code = None
    if request.user.is_staff:
        device, created = TOTPDevice.objects.get_or_create(user=request.user, name="default")
        if not device.confirmed:
            # Generate QR code for TOTP
            totp_uri = device.config_url
            qr = qrcode.make(totp_uri)
            buf = BytesIO()
            qr.save(buf, format='PNG')
            qr_code = base64.b64encode(buf.getvalue()).decode('utf-8')
    if request.method == 'POST':
        form = UserChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form, 'qr_code': qr_code, 'device': device})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password changed!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})
