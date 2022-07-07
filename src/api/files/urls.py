from django.urls import path

from .views import schedule_file_view, download_result_views


urlpatterns = [
    path("schedule_file", schedule_file_view, name="schedule-file"),
    path("file_task/<int:pk>/download", download_result_views, name="download-result"),
]
