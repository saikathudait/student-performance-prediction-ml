from django.contrib import admin
from django.urls import include, path

from predictions import views as prediction_views

admin.site.site_header = "Student Performance Admin"
admin.site.site_title = "Student Performance Admin"
admin.site.index_title = "Administration"

urlpatterns = [
    path("superadmin/", prediction_views.dashboard, name="superadmin"),
    path("superadmin/users/", prediction_views.user_management, name="superadmin_users"),
    path("superadmin/exams/", prediction_views.exam_management, name="superadmin_exams"),
    path("django-admin/", admin.site.urls),
    path("", include("predictions.urls")),
]
