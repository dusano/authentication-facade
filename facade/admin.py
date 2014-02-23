from django.contrib import admin
from facade.models import Mapping


class MappingAdmin(admin.ModelAdmin):
	list_display = ('plug', '_pattern', '_target_url', 'index_page', 'group')

	def _pattern(self, obj):
		if obj.pattern:
			return obj.pattern[:50]
		else:
			return obj.pattern

	def _target_url(self, obj):
		if obj.target_url:
			return obj.target_url[:50]
		else:
			return obj.target_url


admin.site.register(Mapping, MappingAdmin)
