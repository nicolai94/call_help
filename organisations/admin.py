from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from breaks.models.replacements import GroupInfo
from organisations.models import dicts
from organisations.models.groups import Group, Member
from organisations.models.organisations import Organisation, Employee
from users.models.profile import Profile


################################################################
# Inlines
################################################################
class EmployeeInline(TabularInline):
    model = Employee
    fields = ('user', 'position', 'date_joined',)


class MemberInline(TabularInline):
    model = Member
    fields = ('user', 'date_joined',)


class ProfileBreakInline(StackedInline):
    model = GroupInfo
    fields = (
        'min_active',
        'break_start',
        'break_end',
        'break_max_duration',
    )

################################################################
# Models
################################################################


@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')
    # fields = ('name', ) # разрешает поле
    # exclude = ('name', ) # исключает поле
    filter_horizontal = ('employees', ) # делает удобный выбор из списка
    # filter_vertical = ('employees, ')
    inlines = (EmployeeInline, )
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by'
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager')
    list_display_links = ('id', 'name')
    search_fields = ('name', ) # поисковик по полям если добавить __startwith то будет толкьо четкое совпадение
    inlines = (MemberInline, ProfileBreakInline)
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by'
    )


