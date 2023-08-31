# Generated by Django 4.2.4 on 2023-08-31 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EquipmentType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type_title", models.CharField(max_length=255, verbose_name="Тип оборудования")),
                ("sn_mask", models.CharField(max_length=64, verbose_name="Маска для серийного номера")),
            ],
            options={
                "db_table": "equipment_type",
            },
        ),
        migrations.CreateModel(
            name="Equipment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("serial_number", models.CharField(db_index=True, max_length=64, verbose_name="Серийный номер")),
                ("note", models.CharField(max_length=255, verbose_name="Примечание")),
                (
                    "equipment_type_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="equipment",
                        to="equipment.equipmenttype",
                    ),
                ),
            ],
            options={
                "db_table": "equipment",
                "unique_together": {("equipment_type_id", "serial_number")},
            },
        ),
    ]