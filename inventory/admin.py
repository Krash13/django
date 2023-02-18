from django.contrib.admin import site, ModelAdmin
from .models.reagents import Reagents, WorkReagents
from .models.works import Work


class ReagentsModelAdmin(ModelAdmin):
    pass


class WorkReagentsModelAdmin(ModelAdmin):
    pass


class WorkModelAdmin(ModelAdmin):
    pass


site.register(Reagents, ReagentsModelAdmin)
site.register(WorkReagents, WorkReagentsModelAdmin)
site.register(Work, WorkModelAdmin)
