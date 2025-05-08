from django.contrib import admin
from .models import empdata,Service,Rating,Review

admin.site.register(empdata)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'contact_no', 'description', 'address')
    search_fields = ('name', 'service_type', 'address')
    list_filter = ('service_type', 'address')


admin.site.register(Rating)
admin.site.register(Review)