import factory
from metal.models import Steel


class SteelFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Steel

    carbon = 0.1
    manganese = 0
    nickel = 0
    chromium = 0
    molybdenum = 0
    vanadium = 0
    silicon = 0
