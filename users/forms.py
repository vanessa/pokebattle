from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
