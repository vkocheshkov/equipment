
from django.db import models, transaction


class EquipmentType(models.Model):
    """
    Определяет модель данных Тип оборудования. Предполагается, что количество символов в серийном номере не превышает 64
    """
    type_title = models.CharField(max_length=255, null=False, blank=False, verbose_name="Тип оборудования")
    sn_mask = models.CharField(max_length=64, null=False, blank=False, verbose_name="Маска для серийного номера")

    def __str__(self):
        return self.type_title

    class Meta:
        db_table = "equipment_type"


class Equipment(models.Model):
    """
    Определяет модель данных Оборудование. Предполагается, что количество символов в серийном номере не превышает 64.
    Связка тип оборудования и серийный номер должна быть уникальна
    """
    equipment_type_id = models.ForeignKey(EquipmentType, related_name="equipment", on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=64, null=False, blank=False, verbose_name="Серийный номер",
                                     db_index=True)
    note = models.CharField(max_length=255, null=False, blank=False, verbose_name="Примечание")

    def __str__(self):
        return self.serial_number

    class Meta:
        db_table = "equipment"
        unique_together = [["equipment_type_id", "serial_number"]]


