from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import ContactMessage

YES_NO = [("yes", "Yes"), ("no", "No")]


class StudentPredictionForm(forms.Form):
    full_name = forms.CharField(
        label="Full Name",
        max_length=100,
        help_text="Enter the student's full name.",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "e.g., Rahul Sharma",
            "required": True,
        }),
    )
    age = forms.IntegerField(
        label="Age",
        min_value=10,
        max_value=25,
        help_text="Age should be between 10 and 25.",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 10,
            "max": 25,
            "placeholder": "e.g., 16",
            "data-min": 10,
            "data-max": 25,
            "required": True,
        }),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=[("M", "Male"), ("F", "Female")],
        help_text="Select the student's gender.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    school = forms.ChoiceField(
        label="School",
        choices=[("GP", "GP"), ("MS", "MS")],
        help_text="Select the school (GP or MS).",
        widget=forms.Select(attrs={"class": "input"}),
    )
    address = forms.ChoiceField(
        label="Address",
        choices=[("U", "Urban"), ("R", "Rural")],
        help_text="Choose whether the address is Urban or Rural.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    family_size = forms.ChoiceField(
        label="Family Size",
        choices=[("LE3", "LE3"), ("GT3", "GT3")],
        help_text="LE3 = 3 or fewer members, GT3 = more than 3.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    parental_status = forms.ChoiceField(
        label="Parental Status",
        choices=[("T", "Together"), ("A", "Apart")],
        help_text="Select whether parents live together.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    mother_education = forms.IntegerField(
        label="Mother Education (0-4)",
        min_value=0,
        max_value=4,
        help_text="0=None, 1=Primary, 2=Middle, 3=Secondary, 4=Higher.",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 4,
            "placeholder": "0 - 4",
            "data-min": 0,
            "data-max": 4,
        }),
    )
    father_education = forms.IntegerField(
        label="Father Education (0-4)",
        min_value=0,
        max_value=4,
        help_text="0=None, 1=Primary, 2=Middle, 3=Secondary, 4=Higher.",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 4,
            "placeholder": "0 - 4",
            "data-min": 0,
            "data-max": 4,
        }),
    )
    guardian = forms.ChoiceField(
        label="Guardian",
        choices=[("mother", "Mother"), ("father", "Father"), ("other", "Other")],
        help_text="Select the student's primary guardian.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    family_support = forms.ChoiceField(
        label="Family Support",
        choices=YES_NO,
        help_text="Does the family provide academic support?",
        widget=forms.Select(attrs={"class": "input"}),
    )
    internet_access = forms.ChoiceField(
        label="Internet Access",
        choices=YES_NO,
        help_text="Is internet available at home?",
        widget=forms.Select(attrs={"class": "input"}),
    )
    study_time = forms.TypedChoiceField(
        label="Study Time",
        coerce=int,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")],
        help_text="1 = Low, 4 = High study time.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    travel_time = forms.TypedChoiceField(
        label="Travel Time",
        coerce=int,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")],
        help_text="1 = Short, 4 = Long travel time.",
        widget=forms.Select(attrs={"class": "input"}),
    )
    failures = forms.IntegerField(
        label="Failures (0-3)",
        min_value=0,
        max_value=3,
        help_text="Number of past class failures.",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 3,
            "placeholder": "0 - 3",
            "data-min": 0,
            "data-max": 3,
        }),
    )
    absences = forms.IntegerField(
        label="Absences",
        min_value=0,
        max_value=100,
        help_text="Total absences recorded.",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 100,
            "placeholder": "e.g., 5",
            "data-min": 0,
            "data-max": 100,
        }),
    )
    g1 = forms.IntegerField(
        label="G1 (0-20)",
        min_value=0,
        max_value=20,
        help_text="First period grade (0-20).",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 20,
            "placeholder": "0 - 20",
            "data-min": 0,
            "data-max": 20,
        }),
    )
    g2 = forms.IntegerField(
        label="G2 (0-20)",
        min_value=0,
        max_value=20,
        help_text="Second period grade (0-20).",
        widget=forms.NumberInput(attrs={
            "class": "input",
            "min": 0,
            "max": 20,
            "placeholder": "0 - 20",
            "data-min": 0,
            "data-max": 20,
        }),
    )
    activities = forms.ChoiceField(
        label="Extra Activities",
        choices=YES_NO,
        help_text="Does the student join extracurricular activities?",
        widget=forms.Select(attrs={"class": "input"}),
    )
    health = forms.TypedChoiceField(
        label="Health (1-5)",
        coerce=int,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        help_text="1 = Poor, 5 = Excellent.",
        widget=forms.Select(attrs={"class": "input"}),
    )


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label="Full Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Username"}),
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("password1", "password2"):
            self.fields[name].widget.attrs.update({"class": "input"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Username or Email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Password"}),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        if username and "@" in username:
            try:
                user = User.objects.get(email__iexact=username)
                self.cleaned_data["username"] = user.username
            except User.DoesNotExist:
                pass
        return super().clean()


class ContactForm(forms.ModelForm):
    usefulness = forms.TypedChoiceField(
        label="Was the prediction helpful?",
        coerce=int,
        required=False,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        widget=forms.Select(attrs={"class": "input"}),
    )

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message", "usefulness")
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "Email address"}),
            "message": forms.Textarea(
                attrs={"class": "input", "rows": 4, "placeholder": "Write your message"}
            ),
        }
