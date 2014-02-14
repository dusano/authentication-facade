from django.contrib import admin
from facade.models import Mapping


class MappingAdmin(admin.ModelAdmin):
    list_display = ('plug', 'target_url')

admin.site.register(Mapping, MappingAdmin)
