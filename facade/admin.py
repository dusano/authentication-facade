from django.contrib import admin
from facade.models import Mapping


class MappingAdmin(admin.ModelAdmin):
    list_display = ('plug', 'target_url', 'index_page', 'group')

admin.site.register(Mapping, MappingAdmin)
