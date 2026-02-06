from django.urls import path

from . import views

app_name = "predictions"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
    path("model-details/", views.model_details, name="model_details"),
    path("analytics/", views.analytics, name="analytics"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("predict/", views.student_form, name="form"),
    path("result/<int:pk>/", views.result, name="result"),
    path("records/", views.records, name="records"),
    path("history/", views.student_history, name="history"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("profile/", views.profile, name="profile"),
]
