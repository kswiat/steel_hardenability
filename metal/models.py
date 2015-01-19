from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.helpers import inches_to_mm, approximate_diameter
from utils.steel_settings import (CARBON_MIN, CARBON_MAX, MANGANESE_MIN, MANGANESE_MAX, VANADIUM_MAX, NICKEL_MIN,
                                  NICKEL_MAX, CHROMIUM_MIN, CHROMIUM_MAX, MOLYBDENUM_MIN, VANADIUM_MIN, SILICON_MAX,
                                  SILICON_MIN, MOLYBDENUM_MAX)


class Steel(models.Model):
    carbon = models.FloatField(_('carbon'), default=CARBON_MIN,
                               help_text=_("%s - %s") % (CARBON_MIN, CARBON_MAX),
                               validators=[MinValueValidator(CARBON_MIN), MaxValueValidator(CARBON_MAX)])
    manganese = models.FloatField(_('manganese'), default=MANGANESE_MIN,
                                  help_text=_("%s - %s") % (MANGANESE_MIN, MANGANESE_MAX),
                                  validators=[MinValueValidator(MANGANESE_MIN), MaxValueValidator(MANGANESE_MAX)])
    nickel = models.FloatField(_('nickel'), default=NICKEL_MIN,
                               help_text=_("%s - %s") % (NICKEL_MIN, NICKEL_MAX),
                               validators=[MinValueValidator(NICKEL_MIN), MaxValueValidator(NICKEL_MAX)])
    chromium = models.FloatField(_('chromium'), default=CHROMIUM_MIN,
                                 help_text=_("%s - %s") % (CHROMIUM_MIN, CHROMIUM_MAX),
                                 validators=[MinValueValidator(CHROMIUM_MIN), MaxValueValidator(CHROMIUM_MAX)])
    molybdenum = models.FloatField(_('molybdenum'), default=MOLYBDENUM_MIN,
                                   help_text=_("%s - %s") % (MOLYBDENUM_MIN, MOLYBDENUM_MAX),
                                   validators=[MinValueValidator(MOLYBDENUM_MIN), MaxValueValidator(MOLYBDENUM_MAX)])
    vanadium = models.FloatField(_('vanadium'), default=VANADIUM_MIN,
                                 help_text=_("%s - %s") % (VANADIUM_MIN, VANADIUM_MAX),
                                 validators=[MinValueValidator(VANADIUM_MIN), MaxValueValidator(VANADIUM_MAX)])
    silicon = models.FloatField(_('silicon'), default=SILICON_MIN,
                                help_text=_("%s - %s") % (SILICON_MIN, SILICON_MAX),
                                validators=[MinValueValidator(SILICON_MIN), MaxValueValidator(SILICON_MAX)])

    def __unicode__(self):
        return u"%sC-%sMn-%sNi-%sCr-%sMo-%sV-%sSi" % (
            self.carbon, self.manganese, self.nickel, self.chromium,
            self.molybdenum, self.vanadium, self.silicon
        )

    def get_absolute_url(self):
        return reverse('steel_details', kwargs=dict(pk=self.pk))

    @property
    def carbon_mf(self):
        if CARBON_MIN <= self.carbon <= 0.39:
            return 0.54 * self.carbon
        elif 0.39 < self.carbon <= 0.55:
            return 0.171 + 0.001*self.carbon + 0.265*self.carbon**2
        elif 0.55 < self.carbon <= 0.65:
            return 0.115 + 0.268*self.carbon - 0.038*self.carbon**2
        elif 0.65 < self.carbon <= 0.75:
            return 0.143 + 0.2*self.carbon
        elif 0.75 < self.carbon <= CARBON_MAX:
            return 0.062 + 0.409*self.carbon - 0.135*self.carbon**2
        raise Exception("Wrong carbon value")

    @property
    def manganese_mf(self):
        if MANGANESE_MIN <= self.manganese <= 1.2:
            return 3.3333*self.manganese + 1
        elif 1.2 < self.manganese <= MANGANESE_MAX:
            return 5.1*self.manganese - 1.12

    @property
    def silicon_mf(self):
        if SILICON_MIN <= self.silicon <= SILICON_MAX:
            return 1 + 0.7*self.silicon
        raise Exception("Wrong silicon value")

    @property
    def nickel_mf(self):
        if NICKEL_MIN <= self.nickel <= NICKEL_MAX:
            return 1 + 0.363*self.nickel
        raise Exception("Wrong nickel value")

    @property
    def chromium_mf(self):
        if CHROMIUM_MIN <= self.chromium <= CHROMIUM_MAX:
            return 1 + 2.16*self.chromium
        raise Exception("Wrong chromium value")

    @property
    def molybdenum_mf(self):
        if MOLYBDENUM_MIN <= self.molybdenum <= MOLYBDENUM_MAX:
            return 1 + 3.0*self.molybdenum
        raise Exception("Wrong molybdenum value")

    @property
    def vanadium_mf(self):
        if VANADIUM_MIN <= self.vanadium <= VANADIUM_MAX:
            return 1 + 1.73*self.vanadium
        raise Exception("Wrong vanadium value")

    @property
    def ideal_critic_diameter(self):
        d = self.carbon_mf * self.manganese_mf * self.silicon_mf * self.nickel_mf * self.chromium_mf *\
               self.molybdenum_mf * self.vanadium_mf
        return inches_to_mm(d)


class IdealDiameter(models.Model):
    value = models.FloatField(_('value'), default=0, validators=[MinValueValidator(0), MaxValueValidator(500)])
    grain = models.PositiveIntegerField(_('grain'), default=1)
    steel = models.ForeignKey('Steel', verbose_name=_('steel'), related_name='ideal_diameters')

    def __unicode__(self):
        return u"%s mm/grain: %s" % (self.value, self.grain)