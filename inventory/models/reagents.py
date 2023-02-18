from pint import UnitRegistry
from django.db.models import Model, DateTimeField, IntegerField, CharField, FloatField, ForeignKey
from django.db.models.deletion import CASCADE
from .choices import UnitsType
from .works import Work


class Reagents(Model):
    name = CharField(max_length=100, verbose_name='Наименование')
    quantity = FloatField(default=0, verbose_name='Количество')
    units = IntegerField(verbose_name='Единицы измерения', choices=UnitsType.choices)
    place = CharField(max_length=500, default="", verbose_name="Место хранения")
    last_update_date = DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Реагенты'
        verbose_name_plural = 'Реагенты'

    def __str__(self):
        return self.name

    def check_quantity(self, quantity, units):
        ureg = UnitRegistry()
        return self.quantity * ureg[self.get_units_display()] > quantity * ureg[units]

    def minus(self, quantity, units):
        ureg = UnitRegistry()
        new_quantity = self.quantity * ureg[self.get_units_display()] - quantity * ureg[units]
        self.quantity = new_quantity.m
        self.save()

    def plus(self, quantity, units):
        ureg = UnitRegistry()
        new_quantity = self.quantity * ureg[self.get_units_display()] + quantity * ureg[units]
        self.quantity = new_quantity.m
        self.save()


class WorkReagents(Model):
    reagent = ForeignKey(to=Reagents, on_delete=CASCADE, related_name='work_reagents')
    work = ForeignKey(to=Work, on_delete=CASCADE, related_name='reagents')
    quantity = FloatField(default=0, verbose_name='Количество')
    units = IntegerField(verbose_name='Единицы измерения', choices=UnitsType.choices)

    class Meta:
        verbose_name = 'Реагенты для лабораторной работы'
        verbose_name_plural = 'Реагенты для лабораторной работы'

    def __str__(self):
        return "{} ({})".format(self.work.name, self.reagent.name)
