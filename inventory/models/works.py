from django.db.models import Model, CharField, TextField


class Work(Model):
    name = CharField(max_length=100, verbose_name='Наименование')
    description = TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Лабораторная работа'
        verbose_name_plural = 'Лабораторные работы'

    def __str__(self):
        return self.name
