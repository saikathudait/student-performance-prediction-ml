from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from .forms import ContactForm, LoginForm, RegisterForm, StudentPredictionForm
from .models import ContactMessage, StudentPrediction
from .services import predict


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("superadmin")
        return redirect("predictions:student_dashboard")
    return render(request, "predictions/index.html")


@login_required(login_url="predictions:login")
def student_form(request):
    if request.method == "POST":
        form = StudentPredictionForm(request.POST)
        if form.is_valid():
            label, confidence = predict(form.cleaned_data)
            record = StudentPrediction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data["full_name"],
                age=form.cleaned_data["age"],
                gender=form.cleaned_data["gender"],
                school=form.cleaned_data["school"],
                address=form.cleaned_data["address"],
                family_size=form.cleaned_data["family_size"],
                parental_status=form.cleaned_data["parental_status"],
                mother_education=form.cleaned_data["mother_education"],
                father_education=form.cleaned_data["father_education"],
                guardian=form.cleaned_data["guardian"],
                family_support=form.cleaned_data["family_support"],
                internet_access=form.cleaned_data["internet_access"],
                study_time=form.cleaned_data["study_time"],
                travel_time=form.cleaned_data["travel_time"],
                failures=form.cleaned_data["failures"],
                absences=form.cleaned_data["absences"],
                g1=form.cleaned_data["g1"],
                g2=form.cleaned_data["g2"],
                activities=form.cleaned_data["activities"],
                health=form.cleaned_data["health"],
                prediction=label,
                confidence=confidence,
            )
            request.session["last_prediction_id"] = record.id
            return redirect("predictions:result", pk=record.id)
    else:
        form = StudentPredictionForm()

    return render(request, "predictions/student_form.html", {"form": form})


@login_required(login_url="predictions:login")
def result(request, pk=None):
    if pk is None:
        pk = request.session.get("last_prediction_id")
    if not pk:
        return redirect("predictions:form")

    record = get_object_or_404(StudentPrediction, pk=pk)
    if record.user and record.user != request.user and not request.user.is_staff:
        return redirect("predictions:student_dashboard")
    confidence_percent = None
    if record.confidence is not None:
        confidence_percent = round(record.confidence * 100, 2)
    return render(
        request,
        "predictions/result.html",
        {"record": record, "confidence_percent": confidence_percent},
    )


@user_passes_test(lambda u: u.is_staff, login_url="predictions:login")
def records(request):
    history = StudentPrediction.objects.all()
    return render(request, "predictions/records.html", {"records": history})


def about(request):
    return render(request, "predictions/about.html")


def how_it_works(request):
    return render(request, "predictions/how_it_works.html")


def model_details(request):
    return render(request, "predictions/model_details.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received.")
            return redirect("predictions:contact")
    else:
        form = ContactForm()
    return render(request, "predictions/contact.html", {"form": form})


@login_required(login_url="predictions:login")
def analytics(request):
    qs = StudentPrediction.objects.filter(user=request.user)
    result_filter = request.GET.get("result", "").upper()
    if result_filter in {"PASS", "FAIL"}:
        qs = qs.filter(prediction=result_filter)

    start_date = parse_date(request.GET.get("start", "")) if request.GET.get("start") else None
    end_date = parse_date(request.GET.get("end", "")) if request.GET.get("end") else None

    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)

    totals = qs.count()
    pass_count = qs.filter(prediction="PASS").count()
    fail_count = qs.filter(prediction="FAIL").count()
    pass_rate = round((pass_count / totals) * 100, 2) if totals else 0

    recent = qs.order_by("-created_at")[:8]
    chart_data = {
        "labels": ["PASS", "FAIL"],
        "values": [pass_count, fail_count],
    }

    return render(
        request,
        "predictions/analytics.html",
        {
            "records": qs,
            "totals": totals,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "pass_rate": pass_rate,
            "recent": recent,
            "chart_data": chart_data,
        },
    )


@user_passes_test(lambda u: u.is_staff, login_url="predictions:login")
def dashboard(request):
    totals = StudentPrediction.objects.count()
    pass_count = StudentPrediction.objects.filter(prediction="PASS").count()
    fail_count = StudentPrediction.objects.filter(prediction="FAIL").count()
    pass_rate = round((pass_count / totals) * 100, 2) if totals else 0
    recent = StudentPrediction.objects.order_by("-created_at")[:6]
    user_count = get_user_model().objects.count()
    contact_count = ContactMessage.objects.count()

    return render(
        request,
        "predictions/dashboard.html",
        {
            "totals": totals,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "pass_rate": pass_rate,
            "recent": recent,
            "user_count": user_count,
            "contact_count": contact_count,
        },
    )


@user_passes_test(lambda u: u.is_staff, login_url="predictions:login")
def user_management(request):
    User = get_user_model()
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        if action and user_id:
            try:
                target = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("superadmin_users")

            if target == request.user and action in {"toggle_staff", "toggle_active", "toggle_superuser"}:
                messages.error(request, "You cannot change your own admin permissions.")
                return redirect("superadmin_users")

            if action == "toggle_staff":
                target.is_staff = not target.is_staff
                target.save()
                messages.success(request, f"Staff access updated for {target.username}.")
            elif action == "toggle_active":
                target.is_active = not target.is_active
                target.save()
                messages.success(request, f"Active status updated for {target.username}.")
            elif action == "toggle_superuser":
                target.is_superuser = not target.is_superuser
                target.is_staff = True if target.is_superuser else target.is_staff
                target.save()
                messages.success(request, f"Superuser status updated for {target.username}.")

        return redirect("superadmin_users")

    users = User.objects.order_by("-date_joined")
    return render(request, "predictions/user_management.html", {"users": users})


def register(request):
    if request.user.is_authenticated:
        return redirect("predictions:student_dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("predictions:student_dashboard")
    else:
        form = RegisterForm()
    return render(request, "predictions/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("superadmin")
        return redirect("predictions:student_dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if form.get_user().is_staff:
                return redirect("superadmin")
            return redirect("predictions:student_dashboard")
    else:
        form = LoginForm()
    return render(request, "predictions/login.html", {"form": form})


@login_required(login_url="predictions:login")
def logout_view(request):
    logout(request)
    return redirect("predictions:home")


@login_required(login_url="predictions:login")
def student_dashboard(request):
    prediction_count = StudentPrediction.objects.filter(user=request.user).count()
    return render(
        request,
        "predictions/student_dashboard.html",
        {"prediction_count": prediction_count},
    )


@login_required(login_url="predictions:login")
def profile(request):
    prediction_count = StudentPrediction.objects.filter(user=request.user).count()
    return render(
        request,
        "predictions/profile.html",
        {"prediction_count": prediction_count},
    )


@login_required(login_url="predictions:login")
def student_history(request):
    records = StudentPrediction.objects.filter(user=request.user)
    return render(request, "predictions/history.html", {"records": records})
