from django.contrib import admin
from .models import Student

class StudentAdminControl(admin.AdminSite):
    site_header = "Qiao"
    site_title = "QiaoWei"

site = StudentAdminControl()

class StudentAdmin(admin.ModelAdmin):
    list_display = "s_name","s_age","s_hobby"
    search_fields = "s_name",


site.register(Student,StudentAdmin)
