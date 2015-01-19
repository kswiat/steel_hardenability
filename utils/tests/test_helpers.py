from django.test import TestCase
from metal.factories import SteelFactory
from utils.helpers import calculate_di, DE_RETANA, get_f_values, KRAMER


class TestCalculateDi(TestCase):
    def setUp(self):
        self.steel = SteelFactory()
        self.d0 = 0.4
        self.f_values_list = [
            {'content': 0.7, 'element_key': 'Ni', 'f_value': 1.2319584846000002},
            {'content': 0.7, 'element_key': 'Mo', 'f_value': 2.2821349054},
            {'content': 0.7, 'element_key': 'Mn', 'f_value': 2.0730638105999994},
            {'content': 0.7, 'element_key': 'Si', 'f_value': 1.0220654538000002},
            {'content': 0.7, 'element_key': 'Cr', 'f_value': 1.6873583099999998},
        ]

    def test_calculate_di_ni_less_than_1(self):
        expected = 0.4 * 1.2319584846000002 * 2.2821349054 * 2.0730638105999994 * 1.0220654538000002 * \
                   1.6873583099999998

        self.assertEqual(expected, calculate_di(self.d0, self.f_values_list))

    def test_calculate_di_ni_equal_1(self):
        self.f_values_list[0]['content'] = 1
        self.f_values_list.append({'content': 0.7, 'element_key': 'Mo-Ni', 'f_value': 2.9303067429})
        expected = 0.4 * 1.2319584846000002 * 2.2821349054 * 2.0730638105999994 * 1.0220654538000002 * \
                   1.6873583099999998 * 2.9303067429

        self.assertEqual(expected, calculate_di(self.d0, self.f_values_list))

    def test_calculate_di_ni_more_than_1(self):
        self.f_values_list[0]['content'] = 1.01
        self.f_values_list.append({'content': 0.7, 'element_key': 'Mo-Ni', 'f_value': 2.9303067429})
        expected = 0.4 * 1.2319584846000002 * 2.2821349054 * 2.0730638105999994 * 1.0220654538000002 * \
                   1.6873583099999998 * 2.9303067429

        self.assertEqual(expected, calculate_di(self.d0, self.f_values_list))


class TestGetFValuesDeRetana(TestCase):
    def setUp(self):
        self.steel = SteelFactory()

    def test_get_f_values_de_retana(self):
        f_values = get_f_values(self.steel, DE_RETANA)
        self.assertEqual(len(f_values), 5)
        self.assertIn({'content': 0, 'element_key': 'Ni', 'f_value': 0.994214}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Mo', 'f_value': 1.0024}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Mn', 'f_value': 1.0027}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Si', 'f_value': 0.993901}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Cr', 'f_value': 1.0244}, f_values)

    def test_get_f_values_de_retana_random_values(self):
        self.steel.manganese = 0.6
        self.steel.nickel = 0.7
        self.steel.chromium = 1
        self.steel.molybdenum = 0.7
        self.steel.vanadium = 0.7
        self.steel.silicon = 0.7
        self.steel.save()

        f_values = get_f_values(self.steel, DE_RETANA)
        self.assertEqual(len(f_values), 5)
        self.assertIn({'content': 0.7, 'element_key': 'Ni', 'f_value': 1.2319584846000002}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Mo', 'f_value': 2.2821349054}, f_values)
        self.assertIn({'content': 0.6, 'element_key': 'Mn', 'f_value': 1.8776832976000002}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.0220654538000002}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.10282}, f_values)

    def test_get_f_values_de_retana_random_values_Ni_equal_1(self):
        self.steel.manganese = 0.6
        self.steel.nickel = 1
        self.steel.chromium = 1
        self.steel.molybdenum = 0.7
        self.steel.vanadium = 0.7
        self.steel.silicon = 0.7
        self.steel.save()

        f_values = get_f_values(self.steel, DE_RETANA)
        self.assertEqual(len(f_values), 6)
        self.assertIn({'content': 1, 'f_value': 1.324281, 'element_key': 'Ni'},f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Mo', 'f_value': 2.2821349054}, f_values)
        self.assertIn({'content': 0.6, 'element_key': 'Mn', 'f_value': 1.8776832976000002}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.0220654538000002}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.10282}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Mo-Ni', 'f_value': 2.9303067429}, f_values)

    def test_get_f_values_de_retana_random_values_Ni_over_1(self):
        self.steel.manganese = 0.6
        self.steel.nickel = 1.4
        self.steel.chromium = 1
        self.steel.molybdenum = 0.7
        self.steel.vanadium = 0.7
        self.steel.silicon = 0.7
        self.steel.save()

        f_values = get_f_values(self.steel, DE_RETANA)
        self.assertEqual(len(f_values), 6)
        self.assertIn({'content': 1.4, 'f_value': 1.4451086736, 'element_key': 'Ni'},f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Mo', 'f_value': 2.2821349054}, f_values)
        self.assertIn({'content': 0.6, 'element_key': 'Mn', 'f_value': 1.8776832976000002}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.0220654538000002}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.10282}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Mo-Ni', 'f_value': 2.9303067429}, f_values)



class TestGetFValuesKramer(TestCase):
    def setUp(self):
        self.steel = SteelFactory(carbon=0.3, silicon=0.7, chromium=1)

    def test_get_f_values_kramer_Mn_under_15(self):
        self.steel.manganese = 1.2
        self.steel.save()
        f_values = get_f_values(self.steel, KRAMER)

        self.assertEqual(len(f_values), 5)
        self.assertIn({'content': 0, 'element_key': 'Ni', 'f_value': 1.0133}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Mo', 'f_value': 1}, f_values)
        self.assertIn({'content': 1.2, 'element_key': 'Mn<1,5', 'f_value': 2.1168959999999997}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.26855696}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.7142999999999997}, f_values)

    def test_get_f_values_kramer_Mn_equal_15(self):
        self.steel.manganese = 1.5
        self.steel.save()
        f_values = get_f_values(self.steel, KRAMER)
        self.assertEqual(len(f_values), 5)
        self.assertIn({'content': 0, 'element_key': 'Ni', 'f_value': 1.0133}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Mo', 'f_value': 1}, f_values)
        self.assertIn({'content': 1.5, 'element_key': 'Mn<1,5', 'f_value': 2.7428624999999993}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.26855696}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.7142999999999997}, f_values)

    def test_get_f_values_kramer_Mn_over_1_5(self):
        self.steel.manganese = 1.7
        self.steel.save()
        f_values = get_f_values(self.steel, KRAMER)
        self.assertEqual(len(f_values), 5)
        self.assertIn({'content': 0, 'element_key': 'Ni', 'f_value': 1.0133}, f_values)
        self.assertIn({'content': 0, 'element_key': 'Mo', 'f_value': 1}, f_values)
        self.assertIn({'content': 1.7, 'element_key': 'Mn>1,5', 'f_value': 3.162}, f_values)
        self.assertIn({'content': 0.7, 'element_key': 'Si', 'f_value': 1.26855696}, f_values)
        self.assertIn({'content': 1, 'element_key': 'Cr', 'f_value': 2.7142999999999997}, f_values)

