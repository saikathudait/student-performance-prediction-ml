from django.contrib import admin

from .models import ContactMessage, ExamQuestion, ExamResult, StudentPrediction


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


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "correct_option", "points", "is_active")
    list_filter = ("is_active",)
    search_fields = ("text",)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "percentage", "passed", "created_at")
    list_filter = ("passed", "created_at")
    search_fields = ("user__username", "user__email")
