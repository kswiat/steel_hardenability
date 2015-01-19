import json
import os
from django.conf import settings


DE_RETANA = 'DE_RETANA'
KRAMER = 'KRAMER'

ELEMENT_SYMBOLS = {
    DE_RETANA: {
        'Mn': 'manganese',
        'Si': 'silicon',
        'Ni': 'nickel',
        'Mo': 'molybdenum',
        'Cr': 'chromium',
        'Mo-Ni': 'molybdenum',
    },
    KRAMER: {
        'Mn<1,5': 'manganese',
        'Mn>1,5': 'manganese',
        'Si': 'silicon',
        'Ni': 'nickel',
        'Mo': 'molybdenum',
        'Cr': 'chromium',
    }
}

D0_GRAINS = {
    DE_RETANA: range(4, 11),
    KRAMER: range(1, 13)
}

KL_LENGHTS = {
    DE_RETANA: (1.59, 3.17, 4.76, 6.35, 7.94, 9.52, 11.11, 12.7, 14.29, 15.87, 17.46, 19.05, 20.64, 22.22, 23.81, 25.4),
    KRAMER: (
        1.59, 3.17, 4.76, 6.35, 7.94, 9.52, 11.11, 12.7, 14.29, 15.87, 17.46, 19.05, 20.64, 22.22, 23.81, 25.4, 31.75,
        38.1, 44.45, 50.8
    )
}

DE_RETANA_DIR = os.path.join(settings.DE_RETANA_DIR)
KRAMER_DIR = os.path.join(settings.KRAMER_DIR)

JSON_DIRS = {
    'D0': {
        DE_RETANA: os.path.join(DE_RETANA_DIR, 'd0.json'),
        KRAMER: os.path.join(KRAMER_DIR, 'd0.json'),
    },
    'F': {
        DE_RETANA: os.path.join(DE_RETANA_DIR, 'f.json'),
        KRAMER: os.path.join(KRAMER_DIR, 'f.json'),
    },
    'KL': {
        DE_RETANA: os.path.join(DE_RETANA_DIR, 'kl.json'),
        KRAMER: os.path.join(KRAMER_DIR, 'kl.json'),
    }
}


def get_hrc_from_carbon_a255_1(c):
    """
    Returns martensite hardness specified by american A255 standard,
    initial - 100% martensite
    """
    return 35.395 + 6.990 * c + 312.330 * c ** 2 - 821.744 * c ** 3 + 1015.479 * c ** 4 - 538.346 * c ** 5


def get_hrc_from_carbon_a255_2(c):
    """
    Returns martensite hardness specified by american A255 standard,
    initial - 100% martensite
    """
    return 22.974 + 6.214 * c + 356.364 * c ** 2 - 1091.488 * c ** 3 + 1464.880 * c ** 4 - 750.441 * c ** 5


def get_hrc_mj(c):
    """
    Return martensite hardness specified by Justa
    """
    return 60 + 20 * (c ** (1 / 2.0))


def get_f_values(steel, dict_key):
    f_values = []
    with open(JSON_DIRS['F'][dict_key]) as f_file:
        f_data = json.loads(f_file.read())
        for element_key, element_name in ELEMENT_SYMBOLS[dict_key].items():
            f_a_dict = get_a_dict(f_data, element_key)
            content = getattr(steel, element_name)
            if element_key == 'Mn>1,5' and content <= 1.5 or (element_key == 'Mn<1,5' and content > 1.5):
                continue

            elif element_key == 'Mo-Ni' and (0.6 > content > 1 or getattr(steel, 'nickel') < 1):
                continue
            f_value = get_value(content, f_a_dict)
            f_values.append(dict(element_key=element_key, content=content, f_value=f_value))
    return f_values


def calculate_di(_d0, f_values_list):
    di = _d0
    for element in f_values_list:
        di *= element['f_value']
    return di


def get_di_values(f_values, steel, dict_key):
    from metal.models import IdealDiameter
    di_values = []
    with open(JSON_DIRS['D0'][dict_key]) as d0_file:
        d0_data = json.loads(d0_file.read())

        for grain in D0_GRAINS[dict_key]:
            grain_a_list = get_a_dict(d0_data, str(grain))
            d0 = get_value(steel.carbon, grain_a_list)
            di_value = calculate_di(d0, f_values)
            IdealDiameter.objects.create(steel=steel, value=di_value, grain=grain)
            di_values.append(dict(grain=grain, di_value=di_value))
    return di_values


def get_dict_key(carbon):
    if carbon <= 0.25:
        return DE_RETANA
    elif carbon > 0.25:
        return KRAMER
    raise Exception("Wrong carbon value")


def get_di(steel):
    """
    :param steel: Steel model instance
    :return: calculated ideal diameter
    """
    carbon = steel.carbon
    dict_key = get_dict_key(carbon)
    f_values = get_f_values(steel, dict_key)
    di_values = get_di_values(f_values, steel, dict_key)

    return di_values


def get_a_dict(data, key):
    return {k: v[key] for (k, v) in data.items()}


def get_value(content, a_list):
    return a_list['A0'] + a_list['A1'] * content + a_list['A2'] * content ** 2 + a_list['A3'] * content ** 3 + \
           a_list['A4'] * content ** 4


def get_hrc_by_position(hrc_initial, kl):
    return round(hrc_initial / float(kl), 2)


def get_lenghts(steel):
    carbon = steel.carbon
    dict_key = get_dict_key(carbon)
    return map(str, KL_LENGHTS[dict_key])


def get_kl_list(approximated_di, kl_data):
    return (v for (k, v) in kl_data.items() if str(approximated_di) == k).next()


def get_kl_data(steel):
    carbon = steel.carbon
    dict_key = get_dict_key(carbon)

    with open(JSON_DIRS['KL'][dict_key]) as f:
        kl_data = json.loads(f.read())
        diameters = [k for (k, v) in kl_data.items()]
        approximated_di = approximate_diameter(steel.ideal_critic_diameter, diameters)
        kl_list = get_kl_list(approximated_di, kl_data)
    return kl_list


def approximate_diameter(d, d_list):
    d_list = map(float, d_list)
    d_list.sort()
    return (_ for _ in d_list if _ > d).next()


def inches_to_mm(inches):
    return inches * 25.4


