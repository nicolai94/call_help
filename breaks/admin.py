from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from breaks.models.breaks import Break
from breaks.models.dicts import ReplacementStatus, BreakStatus
from breaks.models.replacements import Replacement, ReplacementEmployee, GroupInfo


################################################################
# Inlines
################################################################
class ReplacementEmployeeInline(TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status')


################################################################
# Models
################################################################

@admin.register(GroupInfo)
class GroupInfoAdmin(admin.ModelAdmin):
    list_display = (
        'group', 'break_start', 'break_end'
    )


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'date', 'break_start', 'break_end', 'break_duration')
    # autocomplete_fields = ('group', ) # позволяет втоматически дополнять название поля (***)
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


