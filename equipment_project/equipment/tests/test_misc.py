from django.test import TestCase

from equipment.misc import get_pattern, validate_sn


class TestMisc(TestCase):
    def test_validate_sn(self):
        """
        Проверяет правильность серийных номеров согласно заданной маске
        """
        mask = get_pattern("XXAAAAAXAA")
        self.assertEquals([], validate_sn(["11AAAAABAA", "22AAAAABAA"], mask))
        self.assertNotEquals([], validate_sn(["3XXAAX@Xss"], mask))
