from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class NewUserCreationForm(UserCreationForm):
    """Class to register new user with required fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password_text = 'Ваш пароль должен содержать как минимум 3 символа.'
        self.fields['password1'].help_text = password_text

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')


class UpdateForm(NewUserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
