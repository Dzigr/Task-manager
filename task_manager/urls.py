from django.contrib import admin
from django.urls import path, include
from .views import IndexView, UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', include('task_manager.apps.users.urls')),
]
