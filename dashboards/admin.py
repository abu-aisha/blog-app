from django.contrib import admin
from .models import GroupHierarchy

# Register your models here.

@admin.register(GroupHierarchy)
class GroupHierarchyAdmin(admin.ModelAdmin):
    list_display = ("group", "parent", "level")
    list_filter = ("level",)
    search_fields = ("group__name",)




