from django.contrib import admin
from .models import QueueItem

# Register your models here.

class QueueAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'item_type', 'place_in_line', 'queued_time')

admin.site.register(QueueItem, QueueAdmin)
