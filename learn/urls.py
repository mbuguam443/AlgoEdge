from django.urls import path
from . import views

app_name = 'learn'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/enroll/', views.enroll_course, name='enroll'),
    path('<slug:course_slug>/lesson/<slug:slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
