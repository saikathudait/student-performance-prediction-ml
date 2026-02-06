from django.contrib import admin

from .models import ContactMessage, StudentPrediction


@admin.register(StudentPrediction)
class StudentPredictionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "full_name",
        "age",
        "g1",
        "g2",
        "absences",
        "prediction",
        "created_at",
    )
    list_filter = ("prediction", "created_at")
    search_fields = ("full_name",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "usefulness", "created_at")
    list_filter = ("usefulness", "created_at")
    search_fields = ("name", "email")
