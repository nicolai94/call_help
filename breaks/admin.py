from django.contrib import admin
from django.contrib.admin import TabularInline

from breaks.models.groups import Group
from breaks.models.organisations import Organisation
from breaks.models.replacements import Replacement, ReplacementStatus, ReplacementEmployee


################################################################
# Inlines
################################################################


class ReplacementEmployeeInline(TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status')


################################################################
# Models
################################################################
@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active')


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'date', 'break_start', 'break_end', 'break_duration')
    inlines = (ReplacementEmployeeInline,)


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')
