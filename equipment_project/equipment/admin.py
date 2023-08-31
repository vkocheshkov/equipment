from django.contrib import admin

from equipment.models import Equipment, EquipmentType


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    pass
