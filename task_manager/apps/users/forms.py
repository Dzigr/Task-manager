from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    """Class to register new user with required fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Ваш пароль должен содержать как минимум 3 символа.'

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')
