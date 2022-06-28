from msilib.schema import Media
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic as generic_views

from .forms import CreateCourseForm
from .models import Course, MediaFile

class ListCoursesView(generic_views.ListView):
    template_name = 'courses/list_courses.html'
    model = Course
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['course_set'] = []
        for course in context['object_list']:
            print(type(course))
            course_with_media = course.__dict__
            course_with_media['media_set'] = []
            course_with_media['media_set'].extend(MediaFile.objects.filter(course_id=course.id))
            context['course_set'].append(course_with_media)
        print(context)
        return context

class CreateCourseView(generic_views.FormView):
    template_name = 'courses/create_course.html'
    form_class = CreateCourseForm
    success_url = reverse_lazy('courses:list_courses')

    '''
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    '''

    def form_valid(self, form):
        course = form.save()
        print(course)
        return super().form_valid(form)

class CourseDetailsView(generic_views.DetailView):
    template_engine = 'courses/course_details.html'
    model = Course

def course_detail(request, pk):
    """Muestra una canción en específico"""
    course = Course.objects.get(pk=pk)
    course_html = course.content
    media_files = MediaFile.objects.filter(course_id=course.id)
    for media in media_files:
        course_html = course_html.replace('<image:{}>'.format(media.argument_number), media.html_format())
    return render(request, "courses/course_details.html", {"course": course_html})