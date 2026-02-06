from django.conf import settings
from django.db import models


class StudentPrediction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="predictions",
    )
    full_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1)
    school = models.CharField(max_length=2)
    address = models.CharField(max_length=1)
    family_size = models.CharField(max_length=3)
    parental_status = models.CharField(max_length=1)
    mother_education = models.PositiveSmallIntegerField()
    father_education = models.PositiveSmallIntegerField()
    guardian = models.CharField(max_length=10)
    family_support = models.CharField(max_length=3)
    internet_access = models.CharField(max_length=3)
    study_time = models.PositiveSmallIntegerField()
    travel_time = models.PositiveSmallIntegerField()
    failures = models.PositiveSmallIntegerField()
    absences = models.PositiveSmallIntegerField()
    g1 = models.PositiveSmallIntegerField()
    g2 = models.PositiveSmallIntegerField()
    activities = models.CharField(max_length=3)
    health = models.PositiveSmallIntegerField()
    prediction = models.CharField(max_length=10)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.prediction}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    usefulness = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class ExamSubject(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveSmallIntegerField(default=15)
    pass_percentage = models.PositiveSmallIntegerField(default=40)
    negative_marking = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ExamQuestion(models.Model):
    OPTION_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    points = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:60]


class ExamResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_results",
    )
    subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="results",
    )
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_count = models.PositiveIntegerField()
    wrong_count = models.PositiveIntegerField()
    percentage = models.FloatField()
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.percentage:.1f}%"
