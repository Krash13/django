from django.contrib.admin import site, ModelAdmin
from .models.student_works import StudentWork, StudentWorkReagents


class WorkReagentsModelAdmin(ModelAdmin):
    pass


class WorkModelAdmin(ModelAdmin):
    pass


site.register(StudentWorkReagents, WorkReagentsModelAdmin)
site.register(StudentWork, WorkModelAdmin)
