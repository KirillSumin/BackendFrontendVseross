from django.contrib import admin

# Register your models here.
from core.models import User


@admin.register(User)
class CampaignAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     ('Общее', {'fields': ('full_name', 'pricing_temp', 'short_name', 'is_active', 'start_d', 'finish_d')}),
    #     ('Файлы', {'fields': ('logo', 'tech_task')}),
    # )
    # filter_horizontal = ('is_staff',)
    list_display = ('email', 'first_name', 'last_name', 'created_d')
    # list_filter = ('is_active',)
