from rest_framework.exceptions import ValidationError

from equipment.misc import get_pattern, validate_sn
from equipment.models import EquipmentType, Equipment


def check_serial_numbers_for_errors(serial_number_list, equipment_type):
    errors = []
    mask = EquipmentType.get_equipment_type_mask(equipment_type)
    if mask:
        pattern = get_pattern(mask)
        mask_errors = validate_sn(serial_number_list, pattern)
    
        if mask_errors:
            error_message = "Серийные номера счетчиков " + ",".join(mask_errors) + " не совпадают с маской " + mask
            errors.append(error_message)

        unique_errors = Equipment.check_equipment_exists(serial_number_list, equipment_type)

        if unique_errors:
            error_message = (
                "Серийные номера счетчиков "
                + ",".join(unique_errors)
                + " с типом оборудования "
                + str(equipment_type)
                + " уже присутствуют в базе данных"
            )
            errors.append(error_message)
    else:
        errors.append("Такого типа оборудования не существует")

    return errors






