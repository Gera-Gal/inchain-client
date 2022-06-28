from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('', login_required(views.ListCoursesView.as_view()), name='list_courses'),
    path('create', login_required(views.CreateCourseView.as_view()), name='create_course'),
    path('details/<int:pk>', login_required(views.course_detail), name='course_details'),
]