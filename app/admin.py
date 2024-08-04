from django.contrib import admin

from app import settings


class AdminSite(admin.AdminSite):
    site_header = settings.APP_NAME


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    empty_value_display = settings.ADMIN_EMPTY_VALUE_DISPLAY


admin_site = AdminSite(name=settings.APP_NAME)
