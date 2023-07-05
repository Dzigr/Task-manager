from django.views.generic import ListView
from django.contrib.auth import get_user_model


class UserListView(ListView):
    """List of users from database."""
    model = get_user_model()
    context_object_name = 'users'
    template_name = 'users/main.html'
