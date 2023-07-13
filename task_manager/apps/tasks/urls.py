from django.urls import path
from .views import TaskFilterListView, TaskDetailView, TaskCreateView,\
                   TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskFilterListView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
