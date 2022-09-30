from django.contrib import admin
from .models import CarMake,CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('model_name','model_make','dealer_id','vehicle_type','model_year')
    search_fields = ['model_name','model_make']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('make_name','make_description')
    search_fields = ['make_name']

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)