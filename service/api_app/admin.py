from django.contrib import admin

from api_app.models import PreOrder


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'product', 'size', 'date_ordered')
