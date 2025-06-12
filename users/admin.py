from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
from django import forms

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    actions = ['reset_password_action']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<id>/reset-password/', self.admin_site.admin_view(self.reset_password_view), name='users_customuser_reset_password'),
        ]
        return custom_urls + urls

    def reset_password_action(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can reset other admins' passwords.", level=messages.ERROR)
            return
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one user to reset password.", level=messages.ERROR)
            return
        user = queryset.first()
        return redirect(f'../{user.pk}/reset-password/')
    reset_password_action.short_description = "Reset password for selected admin"

    def reset_password_view(self, request, id):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can reset other admins' passwords.", level=messages.ERROR)
            return redirect('..')
        user = CustomUser.objects.get(pk=id)
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, f"Password for {user.username} has been reset.", level=messages.SUCCESS)
                return redirect('..')
        else:
            form = AdminPasswordChangeForm(user)
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title=f'Reset password for {user.username}',
            opts=self.model._meta,
        )
        return render(request, 'admin/reset_password.html', context)

admin.site.register(CustomUser, CustomUserAdmin)
