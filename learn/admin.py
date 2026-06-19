from django.contrib import admin
from .models import CourseCategory, Course, Lesson, Quiz, Enrollment, Certificate

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'level', 'is_published', 'enrolled_students', 'rating']
    list_filter = ['is_published', 'level', 'category']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_free']
    list_filter = ['course', 'is_free']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completed', 'progress', 'enrolled_at']
    list_filter = ['completed']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'certificate_id', 'issued_at']
