from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, LessonProgress

class CourseListView(ListView):
    model = Course
    template_name = 'learn/courses.html'
    context_object_name = 'courses'
    paginate_by = 12
    def get_queryset(self):
        qs = Course.objects.filter(is_published=True)
        cat = self.request.GET.get('category')
        level = self.request.GET.get('level')
        if cat: qs = qs.filter(category__slug=cat)
        if level: qs = qs.filter(level=level)
        return qs

class CourseDetailView(DetailView):
    model = Course
    template_name = 'learn/course_detail.html'
    context_object_name = 'course'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = self.get_object()
        if self.request.user.is_authenticated:
            ctx['is_enrolled'] = Enrollment.objects.filter(user=self.request.user, course=course).exists()
        return ctx

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'learn/lesson.html'
    context_object_name = 'lesson'
    def get_object(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return get_object_or_404(Lesson, course=course, slug=self.kwargs['slug'])
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lesson = self.get_object()
        ctx['course'] = lesson.course
        enrolled = Enrollment.objects.filter(user=self.request.user, course=lesson.course).exists()
        if not enrolled and not lesson.is_free:
            ctx['locked'] = True
        return ctx

def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user.is_authenticated:
        Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('learn:course_detail', slug=slug)
