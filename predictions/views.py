import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from django.utils import timezone

from .forms import (
    ContactForm,
    ExamQuestionForm,
    ExamSubjectForm,
    LoginForm,
    RegisterForm,
    StudentPredictionForm,
)
from .models import ContactMessage, ExamQuestion, ExamResult, ExamSubject, StudentPrediction
from .services import predict
from .utils import is_rate_limited


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("superadmin")
        return redirect("predictions:student_dashboard")
    return render(request, "predictions/index.html")


@login_required(login_url="predictions:login")
def student_form(request):
    if request.method == "POST":
        if is_rate_limited(request, "predict", limit=12, window=300):
            messages.error(request, "Too many prediction requests. Please wait a few minutes.")
            form = StudentPredictionForm(request.POST)
            return render(request, "predictions/student_form.html", {"form": form})
        form = StudentPredictionForm(request.POST)
        if form.is_valid():
            try:
                label, confidence = predict(form.cleaned_data)
            except Exception:
                messages.error(request, "Prediction service unavailable. Please try again.")
                return render(request, "predictions/student_form.html", {"form": form})
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
            cache.delete("staff_dashboard_stats")
            request.session["last_prediction_id"] = record.id
            return redirect("predictions:result", pk=record.id)
    else:
        form = StudentPredictionForm()

    exam_score = request.session.get("last_exam_percentage")
    return render(
        request,
        "predictions/student_form.html",
        {"form": form, "exam_score": exam_score},
    )


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
    history = StudentPrediction.objects.only(
        "full_name",
        "age",
        "g1",
        "g2",
        "absences",
        "prediction",
        "created_at",
    )
    return render(request, "predictions/records.html", {"records": history})


def about(request):
    return render(request, "predictions/about.html")


def how_it_works(request):
    return render(request, "predictions/how_it_works.html")


def model_details(request):
    return render(request, "predictions/model_details.html")


@login_required(login_url="predictions:login")
def exam_instructions(request):
    subjects = ExamSubject.objects.filter(is_active=True)
    total_questions = ExamQuestion.objects.filter(is_active=True).count()
    time_limit = settings.EXAM_TIME_LIMIT_MINUTES
    pass_percentage = settings.EXAM_PASS_PERCENTAGE
    negative_marking = settings.EXAM_NEGATIVE_MARKING
    exam_in_progress = request.session.get("exam_in_progress", False)
    last_result_id = request.session.get("exam_last_result_id")

    return render(
        request,
        "predictions/exam_instructions.html",
        {
            "subjects": subjects,
            "total_questions": total_questions,
            "time_limit": time_limit,
            "pass_percentage": pass_percentage,
            "negative_marking": negative_marking,
            "exam_in_progress": exam_in_progress,
            "last_result_id": last_result_id,
        },
    )


@login_required(login_url="predictions:login")
def exam(request):
    subject_id = request.GET.get("subject") or request.POST.get("subject_id") or request.session.get("exam_subject_id")
    subject = None
    if subject_id:
        subject = ExamSubject.objects.filter(pk=subject_id, is_active=True).first()

    if not subject:
        messages.error(request, "Please select a valid exam subject.")
        return redirect("predictions:exam_instructions")

    questions = list(ExamQuestion.objects.filter(is_active=True, subject=subject))
    if not questions:
        messages.error(request, "No questions available for the selected subject.")
        return redirect("predictions:exam_instructions")

    time_limit_seconds = subject.time_limit_minutes * 60

    if request.method == "GET":
        if request.session.get("exam_submitted") and request.session.get("exam_last_result_id"):
            if request.GET.get("start") != "1":
                return redirect("predictions:exam_result", pk=request.session["exam_last_result_id"])
            request.session["exam_submitted"] = False

        if not request.session.get("exam_in_progress"):
            if request.GET.get("start") == "1":
                request.session["exam_in_progress"] = True
                request.session["exam_started_at"] = timezone.now().timestamp()
                request.session["exam_token"] = uuid.uuid4().hex
                request.session["exam_subject_id"] = subject.id
            else:
                return redirect("predictions:exam_instructions")

        started_at = request.session.get("exam_started_at")
        if started_at and (timezone.now().timestamp() - started_at) > time_limit_seconds:
            request.session["exam_in_progress"] = False
            request.session.pop("exam_started_at", None)
            request.session.pop("exam_token", None)
            messages.error(request, "Exam time expired. Please start again.")
            return redirect("predictions:exam_instructions")

        return render(
            request,
            "predictions/exam.html",
            {
                "questions": questions,
                "time_limit_seconds": time_limit_seconds,
                "exam_token": request.session.get("exam_token"),
                "subject": subject,
            },
        )

    # POST: Submit exam
    if not request.session.get("exam_in_progress"):
        messages.error(request, "No active exam session found.")
        return redirect("predictions:exam_instructions")

    token = request.POST.get("exam_token")
    if token != request.session.get("exam_token"):
        messages.error(request, "Invalid exam session. Please start again.")
        return redirect("predictions:exam_instructions")

    correct_count = 0
    wrong_count = 0
    total_marks = 0
    score = 0
    for q in questions:
        total_marks += q.points
        answer = request.POST.get(f"question_{q.id}")
        if answer == q.correct_option:
            correct_count += 1
            score += q.points
        else:
            wrong_count += 1
            if subject.negative_marking:
                score -= subject.negative_marking
    score = max(0, score)
    percentage = round((score / total_marks) * 100, 2) if total_marks else 0
    passed = percentage >= subject.pass_percentage

    result = ExamResult.objects.create(
        user=request.user,
        subject=subject,
        score=round(float(score), 2),
        total_questions=len(questions),
        correct_count=correct_count,
        wrong_count=wrong_count,
        percentage=percentage,
        passed=passed,
    )

    request.session["exam_last_result_id"] = result.id
    request.session["exam_submitted"] = True
    request.session["exam_in_progress"] = False
    request.session.pop("exam_started_at", None)
    request.session.pop("exam_token", None)
    request.session.pop("exam_subject_id", None)
    request.session["last_exam_percentage"] = percentage

    return redirect("predictions:exam_result", pk=result.id)


@login_required(login_url="predictions:login")
def exam_result(request, pk):
    result = get_object_or_404(ExamResult, pk=pk, user=request.user)
    return render(request, "predictions/exam_result.html", {"result": result})


@login_required(login_url="predictions:login")
def exam_history(request):
    results = ExamResult.objects.filter(user=request.user).select_related("subject")
    return render(request, "predictions/exam_history.html", {"results": results})


def contact(request):
    if request.method == "POST":
        if is_rate_limited(request, "contact", limit=5, window=3600):
            messages.error(request, "Too many messages. Please try again later.")
            form = ContactForm(request.POST)
            return render(request, "predictions/contact.html", {"form": form})
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete("staff_dashboard_stats")
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

    cache_key = f"analytics:{request.user.id}:{result_filter}:{start_date}:{end_date}"
    stats = cache.get(cache_key)
    if not stats:
        stats = qs.aggregate(
            totals=Count("id"),
            pass_count=Count("id", filter=Q(prediction="PASS")),
            fail_count=Count("id", filter=Q(prediction="FAIL")),
        )
        cache.set(cache_key, stats, 30)

    totals = stats["totals"]
    pass_count = stats["pass_count"]
    fail_count = stats["fail_count"]
    pass_rate = round((pass_count / totals) * 100, 2) if totals else 0

    recent = qs.only(
        "full_name",
        "age",
        "g1",
        "g2",
        "absences",
        "prediction",
        "created_at",
    ).order_by("-created_at")[:8]
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
    cache_key = "staff_dashboard_stats"
    stats = cache.get(cache_key)
    if not stats:
        stats = StudentPrediction.objects.aggregate(
            totals=Count("id"),
            pass_count=Count("id", filter=Q(prediction="PASS")),
            fail_count=Count("id", filter=Q(prediction="FAIL")),
        )
        stats["user_count"] = get_user_model().objects.count()
        stats["contact_count"] = ContactMessage.objects.count()
        cache.set(cache_key, stats, 30)

    totals = stats["totals"]
    pass_count = stats["pass_count"]
    fail_count = stats["fail_count"]
    pass_rate = round((pass_count / totals) * 100, 2) if totals else 0
    recent = StudentPrediction.objects.only(
        "full_name",
        "age",
        "g1",
        "g2",
        "absences",
        "prediction",
        "created_at",
    ).order_by("-created_at")[:6]
    user_count = stats["user_count"]
    contact_count = stats["contact_count"]

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

    users = User.objects.only(
        "id",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    ).order_by("-date_joined")
    return render(request, "predictions/user_management.html", {"users": users})


@user_passes_test(lambda u: u.is_staff, login_url="predictions:login")
def exam_management(request):
    subject_form = ExamSubjectForm()
    question_form = ExamQuestionForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_subject":
            subject_form = ExamSubjectForm(request.POST)
            if subject_form.is_valid():
                subject_form.save()
                messages.success(request, "Subject added successfully.")
                return redirect("superadmin_exams")
        elif action == "add_question":
            question_form = ExamQuestionForm(request.POST)
            if question_form.is_valid():
                question_form.save()
                messages.success(request, "Question added successfully.")
                return redirect("superadmin_exams")

    subjects = ExamSubject.objects.order_by("name")
    results = ExamResult.objects.select_related("user", "subject").order_by("-created_at")[:30]

    return render(
        request,
        "predictions/exam_management.html",
        {
            "subject_form": subject_form,
            "question_form": question_form,
            "subjects": subjects,
            "results": results,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("predictions:student_dashboard")
    if request.method == "POST":
        if is_rate_limited(request, "register", limit=3, window=3600):
            messages.error(request, "Too many registration attempts. Please try again later.")
            form = RegisterForm(request.POST)
            return render(request, "predictions/register.html", {"form": form})
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
        if is_rate_limited(request, "login", limit=5, window=300):
            messages.error(request, "Too many login attempts. Please wait a few minutes.")
            form = LoginForm(request, data=request.POST)
            return render(request, "predictions/login.html", {"form": form})
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
    records = StudentPrediction.objects.filter(user=request.user).only(
        "full_name",
        "age",
        "g1",
        "g2",
        "absences",
        "prediction",
        "created_at",
    )
    return render(request, "predictions/history.html", {"records": records})
