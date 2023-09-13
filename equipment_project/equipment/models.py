from django.db import models
from rest_framework.exceptions import ValidationError


class EquipmentType(models.Model):
    """
    Определяет модель данных Тип оборудования. Предполагается, что количество символов в серийном номере не превышает 64
    """

    type_title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Тип оборудования")
    sn_mask = models.CharField(max_length=64, null=False, blank=False, verbose_name="Маска для серийного номера")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self):
        return self.type_title

    class Meta:
        db_table = "equipment_type"

    @classmethod
    def get_equipment_type_mask(cls, equipment_type):
        """
        Возвращает маску серийного номера передаваемого типа оборудования
        """

        try:
            mask = cls.objects.filter(id=equipment_type).first()
            return mask.sn_mask
        except AttributeError:
            raise ValidationError(f"Ошибка базы данных при поиске типа оборудования {equipment_type}")


class Equipment(models.Model):
    """
    Определяет модель данных Оборудование. Предполагается, что количество символов в серийном номере не превышает 64.
    Связка тип оборудования и серийный номер должна быть уникальна
    """

    equipment_type = models.ForeignKey(EquipmentType, related_name="equipment", on_delete=models.PROTECT)
    serial_number = models.CharField(
        max_length=64, null=False, blank=False, verbose_name="Серийный номер", db_index=True
    )
    note = models.CharField(max_length=255, null=False, blank=False, verbose_name="Примечание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self):
        return self.serial_number

    class Meta:
        db_table = "equipment"
        unique_together = [["equipment_type_id", "serial_number"]]

    @classmethod
    def check_equipment_exists(cls, sn_list, equipment_type):
        errors = []
        for s_number in sn_list:
            if cls.objects.filter(equipment_type=equipment_type, serial_number=s_number).exists():
                errors.append(s_number)
        return errors

    @classmethod
    def add_equipment(cls, data):
        data_for_adding = [
            cls(equipment_type=data.get("equipment_type"), serial_number=sn, note=data.get("note"))
            for sn in data.get("serial_numbers")
        ]
        cls.objects.bulk_create(data_for_adding)
