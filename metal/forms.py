from django import forms
from metal.models import Steel
from utils.steel_settings import (CARBON_MIN, CARBON_MAX, MANGANESE_MIN, MANGANESE_MAX, VANADIUM_MAX, NICKEL_MIN,
                                  NICKEL_MAX, CHROMIUM_MIN, CHROMIUM_MAX, MOLYBDENUM_MIN, VANADIUM_MIN, SILICON_MAX,
                                  SILICON_MIN, MOLYBDENUM_MAX)


class SteelForm(forms.ModelForm):
    class Meta:
        model = Steel
        fields = '__all__'
        widgets = {
            'carbon': forms.NumberInput(attrs={'min': CARBON_MIN, 'MAX': CARBON_MAX, 'step': 0.01}),
            'manganese': forms.NumberInput(attrs=dict(min=MANGANESE_MIN, MAX=MANGANESE_MAX, step=0.01)),
            'nickel': forms.NumberInput(attrs=dict(min=NICKEL_MIN, MAX=NICKEL_MAX, step=0.01)),
            'chromium': forms.NumberInput(attrs=dict(min=CHROMIUM_MIN, MAX=CHROMIUM_MAX, step=0.01)),
            'molybdenum': forms.NumberInput(attrs=dict(min=MOLYBDENUM_MIN, MAX=MOLYBDENUM_MAX, step=0.01)),
            'vanadium': forms.NumberInput(attrs=dict(min=VANADIUM_MIN, MAX=VANADIUM_MAX, step=0.01)),
            'silicon': forms.NumberInput(attrs=dict(min=SILICON_MIN, MAX=SILICON_MAX, step=0.01)),
        }