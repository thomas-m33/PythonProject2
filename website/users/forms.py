from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # using EmailField() here adds some extra validation like making sure the email has an @ symbol

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm): # used in the profile view to handle private post logic
    trusted_users = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter one username per line (or separate with spaces)"
    )

    class Meta:
        model = Profile
        fields = ["posts_private", "trusted_users"]

    def clean_trusted_users(self):
        data = self.cleaned_data["trusted_users"]

        if not data:
            return []

        usernames = data.split()

        users = User.objects.filter(username__in=usernames)

        found_usernames = set(users.values_list("username", flat=True))
        invalid = [u for u in usernames if u not in found_usernames]

        if invalid:
            raise forms.ValidationError(
                f"These users do not exist: {', '.join(invalid)}"
            )

        return users