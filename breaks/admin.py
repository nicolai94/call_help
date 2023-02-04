from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from breaks.models import groups
from breaks.models.breaks import Break
from breaks.models.dicts import ReplacementStatus, BreakStatus
from breaks.models.groups import Group
from breaks.models.organisations import Organisation
from breaks.models.replacements import Replacement, ReplacementEmployee


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
    # fields = ('name', ) # разрешает поле
    # exclude = ('name', ) # исключает поле
    filter_horizontal = ('employees', ) # делает удобный выбор из списка
    # filter_vertical = ('employees, ')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active', 'replacement_count')
    search_fields = ('name', ) # поисковик по полям если добавить __startwith то будет толкьо четкое
    # совпадение


################################################################
# Счетчик кол-ва смен в админке
    def replacement_count(self, obj):  # создал счетчик в адмиинке для подсчета смен в группе
        return obj.replacement_count

    replacement_count.short_description = 'Количество смен' # задал название поля

    def get_queryset(self, request): # создал подсчет и сделал переменную
        queryset = groups.Group.objects.annotate(
            replacement_count=Count('replacements__id')
        )
        return queryset
########################################################################


@admin.register(BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'date', 'break_start', 'break_end', 'break_duration')
    autocomplete_fields = ('group', ) # позволяет втоматически дополнять название поля (***)
    inlines = (ReplacementEmployeeInline,)
    ordering = ('id',)


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('id', 'replacement_link', 'break_start', 'break_end', 'status')  # show columns and fields
    # ordering = ('id', ) # show different ordering
    # list_display = ('__str__', 'id', 'replacement', 'break_start', 'break_end')
    # list_display_links = ('id', 'replacement', 'break_start', 'break_end') # просто ссылка для перехода в модель
    list_filter = ('status',) # фильтр по любому из полей, добавив __ можно фильтровать по внутреннему полю
    # readonly_fields = ('break_start', ) # если нужно только чтение updated_at, created_at
    empty_value_display = 'Unknown' # заменяет неизвестные значениея на текст
    radio_fields = {'status': admin.VERTICAL} # радио кнопки для поля

    def replacement_link(self, obj): # работает как и link_display но с переходом на нужный link
        link = reverse(
            'admin:breaks_replacement_change', args=[obj.replacement.id]
        ) # путь до страницы изменения обьекта
        return format_html('<a href="{}">{}</a>', link, obj.replacement) # передаю html код


