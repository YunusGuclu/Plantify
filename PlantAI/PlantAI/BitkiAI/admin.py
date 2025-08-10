# admin.py

from django.contrib import admin
from .models import Pesticide, Workflow, WorkflowStep, DiseaseInfo

@admin.register(Pesticide)
class PesticideAdmin(admin.ModelAdmin):
    list_display    = ('name', 'price', 'stock', 'is_active', 'created_at')
    list_filter     = ('is_active',)
    search_fields   = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    ordering     = ('-created_at',)

@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display    = ('workflow', 'name', 'order', 'status', 'created_at', 'updated_at')
    list_filter     = ('status', 'workflow')
    ordering        = ('workflow', 'order')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DiseaseInfo)
class DiseaseInfoAdmin(admin.ModelAdmin):
    list_display    = ('class_name', 'disease', 'created_at', 'updated_at')
    search_fields   = ('class_name', 'disease')
    readonly_fields = ('created_at', 'updated_at')
