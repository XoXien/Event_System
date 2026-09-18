from django import forms
from django.contrib.auth.models import User
from .models import Profile

class StudentRegistrationForm(forms.ModelForm):
    student_id = forms.CharField(max_length=50)
    program = forms.CharField(max_length=100)
    year_level = forms.IntegerField(min_value=1, max_value=6)

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"]

        if Profile.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError(
                "This Student ID is already registered."
            )

        return student_id

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                role=Profile.Role.STUDENT,
                student_id=self.cleaned_data["student_id"],
                program=self.cleaned_data["program"],
                year_level=self.cleaned_data["year_level"],
            )

        return user
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ["student_id", "program", "year_level", "profile_image"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if self.user:
            self.user.first_name = self.cleaned_data["first_name"]
            self.user.last_name = self.cleaned_data["last_name"]
            self.user.email = self.cleaned_data["email"]
            self.user.save()
        return profile
