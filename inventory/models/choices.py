from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UnitsType(IntegerChoices):
    MG = 1, _("mg")
    G = 2, _("g")
    KG = 3, _("kg")
    ML = 4,  _("ml")
    L = 5, _("l")
