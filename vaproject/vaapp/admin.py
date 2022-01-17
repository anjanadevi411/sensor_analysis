from django.contrib import admin

# Register your models here.
from .models import Phsensor, Temp, Batch

# def getFieldsModel(model):
#     return [field.name for field in model._meta.get_fields()]

# class PhsensorAdmin(admin.ModelAdmin):
#     list_dispay = getFieldsModel(Phsensor)

# admin.site.register(Phsensor, PhsensorAdmin)
# admin.site.register(Temp)
# admin.site.register(Batch)


@admin.register(Phsensor, Temp, Batch)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]