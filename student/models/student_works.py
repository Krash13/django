from django.db.models import Model, ForeignKey, DateField, BooleanField
from django.db.models.deletion import CASCADE
from clients.models import ClientSystem
from inventory.models import Work, WorkReagents


class StudentWork(Model):
    student = ForeignKey(to=ClientSystem, on_delete=CASCADE, related_name='student_works', verbose_name='Студент')
    work = ForeignKey(to=Work, on_delete=CASCADE, related_name='students', verbose_name='Работа')
    date = DateField()

    class Meta:
        verbose_name = 'Лабораторная работа студента'
        verbose_name_plural = 'Лабораторные работы студента'

    def __str__(self):
        return "{} ({}) {}".format(self.work.name, self.student, self.date.strftime('%d.%m.%y'))

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.id:
            for reagent in self.work.reagents.all():
                super().save(force_insert, force_update, using, update_fields)
                work_reagent = StudentWorkReagents.objects.create(
                    reagent=reagent,
                    student_work=self
                )
                return None
        return super().save(force_insert, force_update, using, update_fields)


class StudentWorkReagents(Model):
    student_work = ForeignKey(to=StudentWork, on_delete=CASCADE, related_name='reagents', verbose_name='Работа')
    reagent = ForeignKey(to=WorkReagents, on_delete=CASCADE, verbose_name='Реагент')
    taken = BooleanField(default=False)

    class Meta:
        verbose_name = 'Реактивы студента'
        verbose_name_plural = 'Реактивы студента'

    def __str__(self):
        return "{} {}".format(self.student_work, self.reagent.reagent.name)

    def take(self):
        if not self.taken and self.reagent.reagent.check_quantity(self.reagent.quantity, self.reagent.get_units_display()):
            self.taken = True
            self.reagent.reagent.minus(self.reagent.quantity, self.reagent.get_units_display())
            self.save()
            return True
        return False
